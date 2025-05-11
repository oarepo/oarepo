#!/bin/bash

cd $(dirname "$0")

set -e

download_module_translations() {
    set -e
    module=$1

    echo "Downloading translations for $module"
    test -d _tmp || mkdir -p _tmp
    if [ -d _tmp/$module ]; then
        rm -rf _tmp/$module
    fi
    cd _tmp
    git clone https://github.com/inveniosoftware/$module.git
    cd $module
    git pull
    # if there is transifex tokenm, use it for tx pull
    # otherwise, use the default one
    if [ -z "$TRANSIFEX_TOKEN" ]; then
        echo "No Transifex token found, using default one"
        tx pull -a -f
    else
        echo "Transifex token found, using it"
        tx pull -a -f --token $TRANSIFEX_TOKEN
    fi

    python setup.py compile_catalog

    # if module is not invenio-vocabularies (it has translations in  the locale folder)
    # but nothing there
    if [ "$module" != "invenio-vocabularies" ]; then
        # remove all translations except for the ones in the locale folder
        find . -name "translations" | grep 'semantic-ui' | while read js_translations ; do
            (
                echo "Compiling js translations from $js_translations"
                set -e
                cd $js_translations
                cd $(echo $module | sed 's/-/_/g')
                mv package.json package.json.bak
                cat package.json.bak | \
                sed 's/"af",//' | \
                sed 's/"ar",//' | \
                sed 's/"gl",//' | \
                sed 's/"rw",//' | \
                sed 's/"en",//' | \
                sed 's/"et_EE",//' >package.json
                npm install
                npm run compile_catalog
            )
        done
    fi
}

cat invenio_modules_with_translations.txt | while read module; do
    (
        download_module_translations $module
    )
done

(
    set -e
    cd _tmp
    rm -rf ../oarepo/collected_translations

    find . -name "*.po" -o -name "*.mo" | \
    grep -v "node_modules" | \
    while read translations ; do
        echo "Copying $translations"
        dn=$(dirname $translations)
        # remove the first part of the path (./invenio-*)
        dn=$(echo $dn | sed 's/^.\/[^/]*\///')
        mkdir -p ../oarepo/collected_translations/$dn
        cp $translations ../oarepo/collected_translations/$dn
    done

    find . -name "*.json" | \
    grep -v "node_modules" | \
    grep "translations.json" | while read js_translations ; do
        echo "Copying $js_translations"
        mkdir -p ../oarepo/collected_translations/$(dirname $js_translations)
        cp $js_translations ../oarepo/collected_translations/$(dirname $js_translations)
    done
)