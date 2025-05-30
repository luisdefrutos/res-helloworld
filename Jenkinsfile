pipeline {
    agent any

     stages {
        stage('Get Code') {
            steps {
                // Obtener código del repo
                git 'https://github.com/luisdefrutos/res-helloworld'
                bat 'dir'
                echo WORKSPACE
            }
        }
    
        stage('Build') {
           steps {
              echo 'Eyyy, esto es Python. No hay que compilar nada!!!'
           }
        }
        
        stage('Tests')
        {
            parallel
            {

                stage('Unit') {
                            steps {
                                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                                    bat '''
                                        set PYTHONPATH=.
                                        pytest --junitxml=result-unit.xml test\\unit
                                    '''
                                }
                            }
                }
                
                        
                stage('Rest') {
                    steps {
                        catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                            bat '''
                                set FLASK_APP=app\\api.py
                                start flask run
                                start java -jar C:\\UNIR\\Ejercicios\\wiremock-standalone-4.0.0-beta.2.jar --port 9090 --root-dir test\\wiremock
                                
                                ping -n 10 127.0.0.1
                                
                                pytest --junitxml=result-rest.xml test\\rest
                            '''
                        }
                    }
                }        
            }
        }
        
        stage ('Results') {
            steps {
                junit 'result*.xml'
            }
        } 
        
        stage('Coverage')
        {
            steps
            {
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                    bat '''
                    set PYTHONPATH=.
                    coverage run --branch --source=app --omit=app\\__init__.py,app\\api.py -m pytest test\\unit
                    coverage xml
                    '''

                    cobertura coberturaReportFile: 'coverage.xml', conditionalCoverageTargets: '100,0,80', lineCoverageTargets: '100,0,80'
                }

            }
        }

        
     }
}