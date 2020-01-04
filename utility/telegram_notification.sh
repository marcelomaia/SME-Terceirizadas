#!/usr/bin/env bash

BOT_URL="https://api.telegram.org/bot${TELEGRAM_TOKEN}/sendMessage"

# Set formatting for the message. Can be either "Markdown" or "HTML"
PARSE_MODE="Markdown"


# typically SUCCESS, UNSTABLE, or FAILURE. Will never be null.
if [ $1 -ne "SUCCESS" ]; then
    build_status="FAILED 👹"
else
    build_status="SUCCEEDED 🤙"
fi

AUTHOR_NAME=$(git show -s --pretty=%an)
COMMIT_MSG=$(git log --format=%B -n 1)

# echo "${BUILD_STATUS_TESTE}"
# echo "Jenkins build #${BUILD_NUMBER} - ${JOB_NAME} - ${AUTHOR} - ${COMMIT_MSG} - ${JOB_DISPLAY_URL} ${BUILD_STATUS} - ${BRANCH_NAME}-  ${GIT_LOCAL_BRANCH} - ${GIT_BRANCH}"
# # Jenkins build #34 - TercTeste - Marcelo Maia - auhdsauhdsuahdsahud - https://jenkins.marcelomaia.tech/job/TercTeste/display/redirect  - -   - origin/development
# echo "First arg:"

send_msg () {
    curl -s -X POST ${BOT_URL} -d chat_id=$TELEGRAM_CHAT_ID \
        -d text="$1" -d parse_mode=${PARSE_MODE}
}

send_msg "
-------------------------------------
Jenkins build #${BUILD_NUMBER} *${build_status}*
\`Job Name:  ${JOB_NAME}\`
\`Branch:      ${GIT_BRANCH}\`
\`Author:      ${AUTHOR_NAME}\`
*Commit Msg:*
${COMMIT_MSG}
[Job Log here](${JOB_DISPLAY_URL})
--------------------------------------
"
