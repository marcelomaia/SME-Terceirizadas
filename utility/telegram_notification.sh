#!/usr/bin/env bash

AUTHOR=$(git show -s --pretty=%an)
COMMIT_MSG=$(git log --format=%B -n 1)

# Use built-in Travis variables to check if all previous steps passed:
# if [ $TRAVIS_TEST_RESULT -ne 0 ]; then
#     build_status="FAILED 👹"
# else
#     build_status="SUCCEEDED 🤙"
# fi

echo "Jenkins build #${BUILD_NUMBER} - ${JOB_NAME} - ${AUTHOR} - ${COMMIT_MSG} - ${JOB_DISPLAY_URL} ${BUILD_STATUS} - ${BRANCH_NAME}-  ${GIT_LOCAL_BRANCH} - ${GIT_BRANCH}"
echo "XXXX ${GIT_COMMITTER_NAME} - ${GIT_AUTHOR_NAME} - ${GIT_COMMITTER_EMAIL} - ${GIT_AUTHOR_EMAIL}"
