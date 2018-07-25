#!/bin/bash -e

debug="True"
frameworkFolder="/var/www/app/src/djangoprj"
timestampFile=".updated_at"

function containers_stopall {
    containers=$(docker ps -q | wc -l | xargs)
    if [[ ${containers} > 1 ]]; then
        docker stop $(docker ps -q)
    else
        echo -e "No containers to stop"
    fi
}

function containers_killall {
    containers=$(docker ps -q | wc -l | xargs)
    if [[ ${containers} > 1 ]]; then
        docker kill $(docker ps -q)
    else
        echo -e "No containers to kill"
    fi
}

function containers_rmall {
    containers=$(docker ps -a -q | wc -l | xargs)
    if [[ ${containers} > 1 ]]; then
        docker rm $(docker ps -a -q)
    else
        echo -e "No containers to delete"
    fi
}

function containers_rmimages {
    containers=$(docker images -q | wc -l | xargs)
    if [[ ${containers} > 1 ]]; then
        docker rmi $(docker images -q)
    else
        echo -e "No images to delete"
    fi
}

function configuration_check {
    check=$(cat ../docker/docker-compose.yml |grep client-project_ | wc -l | xargs)
    if [[ ${check} != 0 ]] && [[ "${command}" != "setprojectname" ]]; then
        echo -e "Please check your docker-compose script or use ${0} setprojectname [client-project] to set a new name"
        echo -e
        usage
        exit 1
    fi
}

function usage {
    echo -e "Usage: ${0} <start|stop|reloadapp|reinstallpkg|collectstatic|connect|getip|stopall|killall|rmall|rmimages|purgeall|setprojectname>"
    echo -e "   start              -> start all the containers defined in docker-compose"
    echo -e "   stop               -> stop all the containers defined in docker-compose"
    echo -e "   reinstallpkg       -> reinstall the pip packages"
    echo -e "   collectstatic | cs -> deploy django static files"
    echo -e "   connect | c        -> connect to a container by name"
    echo -e "   getip              -> get the ip for a container"
    echo -e "   ps                 -> list all containers"
    echo -e "   stopall            -> stop all the containers"
    echo -e "   killall            -> kill all the containers"
    echo -e "   rmall | rmc        -> remove all the containers"
    echo -e "   rmimages |rmi      -> remove all the images"
    echo -e "   purgeall | pall    -> purge all"
    echo -e "   prune              -> remove all unused containers, networks, images"
    echo -e "   setprojectname     -> set the project name for the containers"
}

configuration_check

case ${1} in
    start)
        # Start all the containers defined in docker-compose
        echo -e "Spinning up containers"
        containers=$(docker ps | wc -l | xargs)
        if [[ ${containers} == 1 ]]; then
            cd ../docker
            last_updated=$(ls -ta | head -n 1)
            if [[ "${last_updated}" != "${timestampFile}" ]]; then
                echo -e "Rebuilding containers"
                docker-compose build
                touch ${timestampFile}
            fi
            if [[ "${debug}" = True ]]; then
                docker-compose up
            else
                docker-compose start
            fi
        else
            echo "You already have running containers"
        fi
    ;;

    stop)
        # Start all the containers defined in docker-compose
        containers=$(docker ps | wc -l | xargs)
        if [[ ${containers} > 1 ]]; then
            cd ../docker
            if [[ "${debug}" = True ]]; then
                docker-compose stop
            else
                docker-compose down
            fi
        else
            echo "You don't have running containers"
        fi
    ;;

    reinstallpkg)
        # Reinstall the pip packages (used after pycharm installs his tools)
        # TODO: only for python
        container=$(docker ps | grep _app | awk -F" " '{print $1}')
        docker exec -ti ${container} pip install -r ${frameworkFolder}/requirements.txt
    ;;

    collectstatic | cs)
        # Deploy django static files
        container=$(docker ps | grep _app | awk -F" " '{print $1}')
        docker exec -ti ${container} python ${frameworkFolder}/manage.py collectstatic <<<yes
    ;;

    connect | c)
        # Connect to a container by name
        container=$(docker ps | grep ${2} | awk -F" " '{print $1}')
        if [[ "${container}" != "" ]]; then
            docker exec -ti ${container} /bin/bash
        fi
    ;;

    getip)
        # Get the ip for a container
        container=$(docker ps | grep ${2} | awk -F" " '{print $1}')
        if [[ "${container}" != "" ]]; then
            docker inspect --format '{{ .NetworkSettings.Networks.docker_default.IPAddress }}' ${container}
        fi
    ;;

    ps)
        # List containers
        docker-compose ps
    ;;

    stopall)
        # Stop all the containers
        containers_stopall
    ;;

    killall)
        # Kill all the containers
        containers_killall
    ;;

    restart | r)
        # Restart single container
        container=$(docker ps | grep ${2} | awk -F" " '{print $1}')
        if [[ "${container}" != "" ]]; then
            cd ../docker && docker-compose restart ${2}
        fi
    ;;

    rmall | rmc)
        # Remove all the containers
        containers_rmall
    ;;

    rmimages | rmi)
        # Remove all the images
        containers_rmimages
    ;;

    purgeall | pall)
        # Purge all
        containers_stopall
        containers_killall
        containers_rmall
        containers_rmimages
    ;;

    prune)
        # Remove all unused containers, networks, images
        docker system prune
    ;;

    setprojectname)
        # Read the docker-compose file and modify the containers names
        if [[ "${2}" != "" ]]; then
            find="container_name: client-project_"
            replace="container_name: ${2}_"
            sed -i "" -e "s/${find}/${replace}/" ../docker/docker-compose.yml
            cat ../docker/docker-compose.yml | grep "container_name"
        fi
    ;;

    *)
        usage
esac
