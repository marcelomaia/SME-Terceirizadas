node {
    checkout scm
    def redisImage = docker.image('redis:5.0.5-alpine').run()
    def postgresImage = docker.image('postgres:11.2-alpine').run(
        """-e POSTGRES_DB=${env.POSTGRES_DB} \
          -e POSTGRES_USER=${env.POSTGRES_USER} \
          -e POSTGRES_PASSWORD=${env.POSTGRES_PASSWORD}"""
        )

    docker.image('python:3.6').inside(
        """--link ${postgresImage.id}:db \
         --link ${redisImage.id}:redis \
         --user 0:0 \
         -v $HOME/virtualenvsCache/:/root/.local/share/virtualenvs/"""
        ) {
            stage('Dependencies') {
               sh 'pip install pipenv'
               sh 'pipenv install --skip-lock'
               sh 'pipenv install --dev --skip-lock'
            }
            stage('Test') {
               sh 'pipenv run pytest'
               sh 'pipenv run flake8'
               sh 'pipenv run coverage html'
            }
        }
    stage('Coverage') {
        publishCoverage adapters: [coberturaAdapter('coverage.xml')], sourceFileResolver: sourceFiles('NEVER_STORE')
    }

    stage('Store artifacts') {
        publishHTML([allowMissing: false, alwaysLinkToLastBuild: false, keepAll: false, reportDir: 'htmlcov', reportFiles: 'index.html', reportName: 'Coverage HTML', reportTitles: ''])
    }


    redisImage.stop()
    postgresImage.stop()
}
