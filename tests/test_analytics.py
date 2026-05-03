import pytest
import pandas as pd
import os
from analytics.node_detector import NodeDetector

@pytest.fixture
def sample_csv(tmp_path):
    d = tmp_path / "data"
    d.mkdir()
    p = d / "test_data.csv"
    # N2 has more failures (10) than N1 (6)
    data = {
        'Nodo': ['N1']*6 + ['N2']*10,
        'Tipo_Falla': ['F1']*16,
        'Minutos_Resolucion': list(range(6)) + list(range(100, 110)),
        'Prioridad': ['Alta']*16
    }
    df = pd.DataFrame(data)
    df.to_csv(p, index=False)
    return str(p)

def test_node_detector_flow(sample_csv):
    detector = NodeDetector(n_clusters=2, min_fallas=3)
    perfiles = detector.load_and_preprocess(sample_csv)
    
    assert len(perfiles) == 2
    
    anomalias = detector.detect_anomalies()
    assert not anomalias.empty
    # N2 has 10 failures, N1 has 6. N2 should be in the critical group.
    assert anomalias.iloc[0]['Nodo'] == 'N2'

def test_node_detector_empty_data():
    detector = NodeDetector()
    with pytest.raises(ValueError, match="No hay datos cargados"):
        detector.detect_anomalies()
