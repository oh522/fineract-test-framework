pipeline {
    agent any

    environment {
        TEST_ENV   = "test"
        ALLURE_DIR = "reports/allure-results"
        REPORT_DIR = "reports/allure-report"
        WECHAT_WEBHOOK = credentials('wechat-webhook-token')  // Jenkins 凭据管理
    }

    triggers {
        // 代码提交自动触发（小林coding第一步）
        githubPush()
        // 也可以定时触发
        cron('H 9 * * 1-5')  // 工作日早9点
    }

    stages {

        stage('① 拉取最新代码') {
            steps {
                checkout scm
                echo "分支: ${env.BRANCH_NAME} | 提交: ${env.GIT_COMMIT[0..7]}"
            }
        }

        stage('② 安装依赖') {
            // 小林coding第二步
            steps {
                sh "pip install -r requirements.txt -q"
            }
        }

        stage('③ 执行测试用例') {
            // 小林coding第三步
            steps {
                sh """
                    mkdir -p ${ALLURE_DIR}
                    pytest api_test/testcase/ \\
                        -v \\
                        -n auto \\
                        --reruns=2 \\
                        --reruns-delay=1 \\
                        --alluredir=${ALLURE_DIR} \\
                        --tb=short \\
                        -m "smoke or P0" \\
                        2>&1 | tee reports/run.log
                """
            }
            post {
                always {
                    // 保存原始日志
                    archiveArtifacts artifacts: 'reports/run.log'
                }
            }
        }

        stage('④ 生成 Allure 报告') {
            // 小林coding第四步
            steps {
                sh "allure generate ${ALLURE_DIR} -o ${REPORT_DIR} --clean"
                allure([
                    includeProperties: false,
                    results: [[path: "${ALLURE_DIR}"]]
                ])
            }
        }

        stage('⑤ 发送测试报告通知') {
            // 小林coding第五步：发送企业微信通知
            steps {
                script {
                    // 解析测试结果
                    def log = readFile('reports/run.log')
                    def passed = (log =~ /(\d+) passed/).findAll()
                    def failed = (log =~ /(\d+) failed/).findAll()
                    def total  = (log =~ /(\d+) total/).findAll()

                    def passCount  = passed  ? passed[0][1]  : "0"
                    def failCount  = failed  ? failed[0][1]  : "0"
                    def totalCount = total   ? total[0][1]   : "?"
                    def status     = failCount == "0" ? "✅ 全部通过" : "❌ 存在失败"

                    // 发企业微信机器人
                    sh """
                        curl -X POST '${WECHAT_WEBHOOK}' \\
                          -H 'Content-Type: application/json' \\
                          -d '{
                            "msgtype": "markdown",
                            "markdown": {
                              "content": "## Fineract 接口测试报告\\n> **状态**: ${status}\\n> **分支**: ${env.BRANCH_NAME}\\n> **总数**: ${totalCount} | **通过**: ${passCount} | **失败**: ${failCount}\\n> [查看详细报告](${env.BUILD_URL}allure)"
                            }
                          }'
                    """
                }
            }
        }
    }

    post {
        failure {
            echo "❌ 流水线失败，请检查测试报告"
        }
        always {
            // 清理超过7天的报告
            sh "find reports/ -mtime +7 -delete || true"
        }
    }
}