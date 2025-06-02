
pipeline {
    agent none

    stages {
        stage('Get Code') {
            agent { label 'test-agent' }
            steps {
                echo "Ejecutando pipeline en rama: ${env.BRANCH_NAME}"
                bat 'dir'
                echo "Ruta del WORKSPACE: ${env.WORKSPACE}"
            }
        }

        stage('Tests') {
            parallel {
                stage('Unit') {
                    agent { label 'test-agent' }
                    steps {
                        bat 'whoami'
                        bat 'hostname'
                        catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                            bat '''
                                cd %WORKSPACE%
                                set PYTHONPATH=.
                                pytest --junitxml=result-unit.xml test\\unit
                            '''
                        }
                        stash includes: 'result-unit.xml', name: 'unit-results'
                    }
                }

                stage('Rest') {
                    agent { label 'flask-agent' }
                    steps {
                        bat 'whoami'
                        bat 'hostname'
                        catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                            bat '''
                                cd %WORKSPACE%
                                set FLASK_APP=app\\api.py
                                start flask run
                                start java -jar C:\\UNIR\\Ejercicios\\wiremock-standalone-4.0.0-beta.2.jar --port 9090 --root-dir test\\wiremock
                                ping -n 10 127.0.0.1
                                pytest --junitxml=result-rest.xml test\\rest
                            '''
                        }
                        stash includes: 'result-rest.xml', name: 'rest-results'
                    }
                }
            }
        }

        stage('Results') {
         agent any
            steps {
                unstash 'unit-results'
                unstash 'rest-results'
                junit 'result*.xml'
            }
        }

        stage('Flake8') {
            agent { label 'test-agent' }
            steps {
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                    bat '''
                        cd %WORKSPACE%
                        flake8 app > result-flake8.txt
                        type result-flake8.txt
                    '''
                }
            }
        }

        stage('Coverage') {
            agent { label 'test-agent' }
            steps {
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                    bat '''
                        cd %WORKSPACE%
                        set PYTHONPATH=.
                        coverage run --branch --source=app --omit=app\\__init__.py,app\\api.py -m pytest test\\unit
                        coverage xml
                        coverage html
                    '''
                    cobertura coberturaReportFile: 'coverage.xml', conditionalCoverageTargets: '100,0,80', lineCoverageTargets: '100,0,80'
                }
            }
        }

        stage('Bandit') {
            agent { label 'test-agent' }
            steps {
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                    echo 'Analizando seguridad con Bandit...'
                    bat 'bandit -r app > result-bandit.txt'
                    bat 'type result-bandit.txt'
                }
            }
        }

        stage('Rendimiento - JMeter') {
            agent { label 'test-agent' }
            steps {
                catchError(buildResult: 'UNSTABLE', stageResult: 'FAILURE') {
                    echo 'Ejecutando prueba de rendimiento con JMeter...'
                    bat '''
                        "C:\\jmeter\\apache-jmeter-5.6.3\\bin\\jmeter.bat" -n -t jmeter\\jmeter-test.jmx -l jmeter-report.jtl
                        type jmeter-report.jtl
                    '''
                }
            }
        }
    }
}

