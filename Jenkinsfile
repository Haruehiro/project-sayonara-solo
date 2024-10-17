node {
    // Define the environment variables
    env.PROJECT_NAME = 'Project-Sayonara'
    env.BUILD_ID = '1'

    try {
        stage('Checkout') {
            // Checkout source code from version control system
            checkout scm
        }

        stage('Build') {
            // Add commands to build your project
            echo 'Building!'
            // Example for a Maven project: sh 'mvn clean package'
        }

        stage('Test') {
            // Run tests here
            echo 'Testing!'
            // Example for a Maven project: sh 'mvn test'
        }

        stage('Deploy') {
            // Deploy your application
            echo 'Deploying!'
            // Example deployment command
            // sh './deploy.sh'
        }
    } catch (e) {
        // If there's an error in any stage, catch it and mark the build as failed
        currentBuild.result = 'FAILED'
        throw e
    } finally {
        // Post-build actions; cleanup, notifications, etc.
        stage('Cleanup') {
            echo 'Cleaning up...'
        }
    }
}
