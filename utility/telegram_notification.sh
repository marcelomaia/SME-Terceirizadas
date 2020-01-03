#!/usr/bin/env bash

AUTHOR=$(git show -s --pretty=%an)
COMMIT_MSG=$(git log --format=%B -n 1)

# Get the token from Travis environment vars and build the bot URL:
BOT_URL="https://api.telegram.org/bot${TELEGRAM_TOKEN}/sendMessage"

# Set formatting for the message. Can be either "Markdown" or "HTML"
PARSE_MODE="Markdown"

# Use built-in Travis variables to check if all previous steps passed:
if [ $TRAVIS_TEST_RESULT -ne 0 ]; then
    build_status="FAILED 👹"
else
    build_status="SUCCEEDED 🤙"
fi

# Define send message function. parse_mode can be changed to
# HTML, depending on how you want to format your message:
send_msg () {
    echo $1
    # curl -s -X POST ${BOT_URL} -d chat_id=$TELEGRAM_CHAT_ID \
        # -d text="$1" -d parse_mode=${PARSE_MODE}
}

# Send message to the bot with some pertinent details about the job
# Note that for Markdown, you need to escape any backtick (inline-code)
# characters, since they're reserved in bash
send_msg "
-------------------------------------
Jenkins build #${env.BUILD_NUMBER} *${build_status}*
\`Job Name:  ${env.JOB_NAME}\`
\`Branch:      ${TRAVIS_BRANCH}\`
\`Author:      ${AUTHOR}\`
*Commit Msg:*
${COMMIT_MSG}
[Job Log here](${env.JOB_DISPLAY_URL})
--------------------------------------
"
