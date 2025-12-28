pipeline {
    agent any
    
    stages {
        stage('Check') {
            steps {
                echo 'Checking environment...'
                sh 'docker compose version'
            }
        }
        
        stage('Start Databases') {
            steps {
                echo 'Starting databases...'
                sh '''
                    cd /workspace
                    # Check if containers are already running
                    if [ ! "$(docker ps -q -f name=mysql_source)" ]; then
                        echo "Starting MySQL..."
                        COMPOSE_PROJECT_NAME=jenkins_project docker compose up -d mysql
                    else
                        echo "MySQL already running"
                    fi
                    
                    if [ ! "$(docker ps -q -f name=postgres_warehouse)" ]; then
                        echo "Starting PostgreSQL..."
                        COMPOSE_PROJECT_NAME=jenkins_project docker compose up -d postgres
                    else
                        echo "PostgreSQL already running"
                    fi
                    
                    echo "Waiting for databases..."
                    sleep 10
                '''
            }
        }
        
        stage('Run ETL') {
            steps {
                echo 'Running ETL...'
                sh 'cd /workspace && COMPOSE_PROJECT_NAME=jenkins_project docker compose run --rm etl'
            }
        }
        
        stage('Run dbt') {
            steps {
                echo 'Running dbt models...'
                sh '''
                    # Get the host path from Jenkins container mount
                    HOSTPATH=$(docker inspect jenkins_cicd --format '{{ range .Mounts }}{{ if eq .Destination "/workspace" }}{{ .Source }}{{ end }}{{ end }}')
                    echo "Host path: $HOSTPATH"
                    
                    docker run --rm \
                    --network jenkins_project_etl_network \
                    -v "${HOSTPATH}/dbt_project:/usr/app" \
                    -v "${HOSTPATH}/dbt_project/profiles.yml:/root/.dbt/profiles.yml" \
                    -w /usr/app \
                    ghcr.io/dbt-labs/dbt-postgres:1.7.4 \
                    run --profiles-dir /root/.dbt --project-dir /usr/app
                '''
            }
        }
        
        stage('Validate') {
            steps {
                echo 'Checking data...'
                sh 'docker exec postgres_warehouse psql -U warehouse_user -d warehouse_db -c "SELECT COUNT(*) FROM raw_data;"'
            }
        }
    }
    
    post {
        success {
            echo '✅ Pipeline Success!'
        }
        failure {
            echo '❌ Pipeline Failed!'
        }
    }
}
