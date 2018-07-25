#!/bin/bash -e

modules=""
moduleList=""

frameworkFolder="/var/www/app/src/djangoprj"
nodeModulesFolder="${frameworkFolder}/node_modules"

cd ${frameworkFolder}

modules=$(find ${frameworkFolder} -depth -type d -not -path "${frameworkFolder}/node_modules/*" -not -path "${frameworkFolder}/public/*" -not -path "${frameworkFolder}/resources/*" -not -path "${frameworkFolder}/static/*" -not -path "${frameworkFolder}/media/*" -name 'assets' -exec dirname {} \; | sort -u)

for module in ${modules}; do
    module=$(dirname ${module})
    currentModule=${module##*/}

    if [[ "${currentModule}" != "djangoprj" ]]; then
        moduleList="${moduleList},${currentModule}"
    fi
done

if [[ ${moduleList/,} != "" ]]; then
    ${nodeModulesFolder}/.bin/gulp dev --modules ${moduleList/,}
else
    ${nodeModulesFolder}/.bin/gulp dev
fi
