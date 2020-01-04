#!/usr/bin/env bash

BOT_URL="https://api.telegram.org/bot${TELEGRAM_TOKEN}/sendMessage"

# Set formatting for the message. Can be either "Markdown" or "HTML"
PARSE_MODE="Markdown"


# typically SUCCESS, UNSTABLE, or FAILURE. Will never be null.
if [ $1 -ne "SUCCESS" ]; then
    tests_status="FAILED 👹"
else
    tests_status="SUCCEEDED 🤙"
fi

if [ $2 -ne "SUCCESS" ]; then
    build_status="FAILED 👹"
else
    build_status="SUCCEEDED 🤙"
fi

if [ $3 -ne "SUCCESS" ]; then
    publish_status="FAILED 👹"
else
    publish_status="SUCCEEDED 🤙"
fi

AUTHOR_NAME=$(git show -s --pretty=%an)
COMMIT_MSG=$(git log --format=%B -n 1)

send_msg () {
    curl -s -X POST ${BOT_URL} -d chat_id=$TELEGRAM_CHAT_ID \
        -d text="$1" -d parse_mode=${PARSE_MODE}
}

send_msg "
-------------------------------------
Jenkins build #${BUILD_NUMBER}
\`Tests:      *${tests_status}*\`
\`Build:      *${build_status}*\`
\`Publish:    *${publish_status}*\`
\`Job Name:    ${JOB_NAME}\`
\`Branch:      ${GIT_BRANCH}\`
\`Author:      ${AUTHOR_NAME}\`
*Commit Msg:*
${COMMIT_MSG}
[Job Log here](${RUN_DISPLAY_URL})
--------------------------------------
"
