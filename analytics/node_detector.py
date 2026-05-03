import pandas as pd
import numpy as np
import logging
from typing import Optional, Tuple
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class NodeDetector:
    """
    Servicio de detección de anomalías en nodos de red utilizando Clustering K-Means.
    """
    def __init__(self, n_clusters: int = 3, min_fallas: int = 5):
        self.n_clusters = n_clusters
        self.min_fallas = min_fallas
        self.scaler = StandardScaler()
        self.kmeans = KMeans(n_clusters=self.n_clusters, random_state=42, n_init=10)
        self.perfiles_nodos: Optional[pd.DataFrame] = None

    def load_and_preprocess(self, file_path: str) -> pd.DataFrame:
        """
        Carga los datos y genera perfiles de salud por nodo.
        """
        try:
            logger.info(f"Cargando datos desde {file_path}")
            df = pd.read_csv(file_path)
            
            # Agregación de perfiles
            perfiles = df.groupby('Nodo').agg(
                Total_Fallas=('Tipo_Falla', 'count'),
                Tiempo_Promedio_Minutos=('Minutos_Resolucion', 'mean'),
                Fallas_Criticas=('Prioridad', lambda x: (x.str.upper() == 'ALTA').sum() + (x.str.upper() == 'CRÍTICA').sum())
            ).reset_index()

            perfiles['Porcentaje_Critico'] = (perfiles['Fallas_Criticas'] / perfiles['Total_Fallas']) * 100
            
            # Filtrado de ruido
            self.perfiles_nodos = perfiles[perfiles['Total_Fallas'] > self.min_fallas].reset_index(drop=True)
            logger.info(f"Evaluando {len(self.perfiles_nodos)} nodos tras filtrado.")
            
            return self.perfiles_nodos
            
        except FileNotFoundError:
            logger.error(f"Archivo no encontrado: {file_path}")
            raise
        except Exception as e:
            logger.error(f"Error en el preprocesamiento: {e}")
            raise

    def detect_anomalies(self) -> pd.DataFrame:
        """
        Ejecuta el algoritmo de clustering para identificar nodos críticos.
        """
        if self.perfiles_nodos is None or self.perfiles_nodos.empty:
            raise ValueError("No hay datos cargados para analizar.")

        sensores = self.perfiles_nodos[['Total_Fallas', 'Tiempo_Promedio_Minutos', 'Porcentaje_Critico']]
        sensores_escalados = self.scaler.fit_transform(sensores)

        # Aplicar K-Means
        self.perfiles_nodos['Grupo_IA'] = self.kmeans.fit_predict(sensores_escalados)

        # Identificar el grupo crítico (mayor promedio de fallas)
        promedios_grupos = self.perfiles_nodos.groupby('Grupo_IA')['Total_Fallas'].mean()
        grupo_critico = promedios_grupos.idxmax()

        nodos_en_peligro = self.perfiles_nodos[self.perfiles_nodos['Grupo_IA'] == grupo_critico]
        logger.info(f"Detección completada. {len(nodos_en_peligro)} nodos en zona crítica.")
        
        return nodos_en_peligro.sort_values(by='Total_Fallas', ascending=False)

if __name__ == "__main__":
    # Ejemplo de uso/test
    detector = NodeDetector()
    try:
        # Asumiendo que el archivo está en el directorio actual o ruta relativa
        nodos_criticos = detector.load_and_preprocess('datos_jira_regresion.csv')
        resultados = detector.detect_anomalies()
        print("\nTOP 10 NODOS CRÍTICOS:")
        print(resultados.head(10)[['Nodo', 'Total_Fallas', 'Porcentaje_Critico']])
    except Exception as e:
        logger.error(f"Fallo en la ejecución: {e}")
