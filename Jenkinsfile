node {
    checkout scm

    sh 'printenv'

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
               sh 'pipenv run pytest --numprocesses=1'
               sh 'pipenv run flake8'
               sh 'utility/verifica_import_relativo.sh'
               sh 'pipenv run coverage html'
            }
        }

    stage('Artifacts') {
        publishCoverage adapters: [coberturaAdapter('coverage.xml')], sourceFileResolver: sourceFiles('NEVER_STORE')
        junit 'Junit.xml'
        publishHTML([allowMissing: false, alwaysLinkToLastBuild: false, keepAll: false, reportDir: 'htmlcov', reportFiles: 'index.html', reportName: 'Relatorio Cobertura HTML', reportTitles: ''])
    }

    redisImage.stop()
    postgresImage.stop()

    sh 'chmod +x /utility/telegram_notification.sh'
    sh './utility/telegram_notification.sh'
}
