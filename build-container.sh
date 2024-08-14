#!/bin/bash

BUILD_FLAG=false
POPULATE_FLAG=false
CONFLICT_FLAG=false

for arg in "$@"
do
    case $arg in
        -build)
        BUILD_FLAG=true
        shift 
        ;;
        -populate)
        POPULATE_FLAG=true
        shift 
        ;;
    esac
done

if [ "$POPULATE_FLAG" = true ]; then
    NEW_POPULATE_VALUE="TRUE"
else
    NEW_POPULATE_VALUE="FALSE"
fi

if grep -q 'POPULATE =' .env; then
    CURRENT_POPULATE_VALUE=$(grep 'POPULATE =' .env | cut -d'=' -f2 | tr -d ' "')
    if [ "$CURRENT_POPULATE_VALUE" != "$NEW_POPULATE_VALUE" ]; then
        CONFLICT_FLAG=true
    fi
else
    CONFLICT_FLAG=true
fi

echo "Setting POPULATE to $NEW_POPULATE_VALUE"
if grep -q 'POPULATE =' .env; then
    sed -i '' "s/POPULATE = .*/POPULATE = \"$NEW_POPULATE_VALUE\"/" .env
else
    echo "POPULATE = \"$NEW_POPULATE_VALUE\"" >> .env
fi

if [ "$BUILD_FLAG" = true ] || [ "$CONFLICT_FLAG" = true ]; then
    echo "Building and starting containers..."
    docker-compose -f dev.docker-compose.yml up --build -d
else
    echo "Starting containers..."
    docker-compose -f dev.docker-compose.yml up -d
fi

echo "Script execution completed."
