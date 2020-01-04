#!/usr/bin/env bash

AUTHOR=$(git show -s --pretty=%an)
COMMIT_MSG=$(git log --format=%B -n 1)

# Use built-in Travis variables to check if all previous steps passed:
# if [ $TRAVIS_TEST_RESULT -ne 0 ]; then
#     build_status="FAILED 👹"
# else
#     build_status="SUCCEEDED 🤙"
# fi
# typically SUCCESS, UNSTABLE, or FAILURE. Will never be null.
echo "${BUILD_STATUS_TESTE}"
echo "Jenkins build #${BUILD_NUMBER} - ${JOB_NAME} - ${AUTHOR} - ${COMMIT_MSG} - ${JOB_DISPLAY_URL} ${BUILD_STATUS} - ${BRANCH_NAME}-  ${GIT_LOCAL_BRANCH} - ${GIT_BRANCH}"
# Jenkins build #34 - TercTeste - Marcelo Maia - auhdsauhdsuahdsahud - https://jenkins.marcelomaia.tech/job/TercTeste/display/redirect  - -   - origin/development
echo "First arg:"
