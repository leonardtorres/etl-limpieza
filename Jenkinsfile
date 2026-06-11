pipeline {
    agent any

    triggers {
        // Opción: Revisa el repositorio cada 5 minutos en busca de cambios (opcional si no usas Webhooks)
        pollSCM('*/5 * * * *') 
    }

    environment {
        // Definimos un entorno virtual de Python para aislar las dependencias
        VENV_DIR = '.venv'
    }

    stages {
        stage('Clonar Repositorio') {
            steps {
                echo 'Clonando el repositorio desde GitHub...'
                // Jenkins descarga automáticamente el código si el pipeline está vinculado al repo,
                // pero esto asegura que limpie la zona de trabajo.
                cleanWs()
                checkout scm
            }
        }

        stage('Preparar Entorno (Build)') {
            steps {
                echo 'Creando el entorno virtual e instalando dependencias...'
                sh '''
                    python3 -m venv $VENV_DIR
                    . $VENV_DIR/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Limpieza y Linteado (Lint)') {
            steps {
                echo 'Ejecutando herramientas de calidad de código...'
                // black formatea el código automáticamente, flake8 busca errores de estilo
                sh '''
                    . $VENV_DIR/bin/activate
                    black src/ tests/
                    flake8 src/ tests/ --max-line-length=88
                '''
            }
        }

        stage('Pruebas Unitarias (Test)') {
            steps {
                echo 'Ejecutando pruebas con PyTest...'
                sh '''
                    . $VENV_DIR/bin/activate
                    pytest tests/ --junitxml=results.xml
                '''
            }
        }

        stage('Ejecutar Aplicación (Run)') {
            steps {
                echo 'Ejecutando la aplicación principal...'
                sh '''
                    . $VENV_DIR/bin/activate
                    python src/main.py
                '''
            }
        }
    }

    post {
        always {
            echo 'Archivando resultados de las pruebas...'
            // Publica los resultados de los tests en la interfaz de Jenkins
            junit allowEmptyResults: true, testResults: 'results.xml'
            
            echo 'Limpiando archivos temporales de Python...'
            // Elimina cachés de python para mantener el servidor limpio
            sh 'find . -type d -name "__pycache__" -exec rm -r {} + 2>/dev/null || true'
        }
        success {
            echo '¡El pipeline se ejecutó con éxito! El código es estable.'
        }
        failure {
            echo 'El pipeline ha fallado. Revisa los logs de los stages anteriores.'
        }
    }
}