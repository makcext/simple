case $1 in
  build)
    docker compose -f build/dev/docker-compose.yml -p simple build --no-cache
    ;;
  start)
    docker compose -f build/dev/docker-compose.yml -p simple up -d simple
    ;;
  restart)
    docker compose -f build/dev/docker-compose.yml -p simple down
    docker compose -f build/dev/docker-compose.yml -p simple up -d simple
    ;;

  stop)
    docker compose -f build/dev/docker-compose.yml -p simple down
    ;;
  shell)
    docker exec -ti simple bash -l
    ;;
  shell_plus)
    docker exec -ti simple ./manage.py shell_plus
    ;;
  pip-compile)
    docker exec -ti simple bash -c "pip-compile --upgrade -r requirements/common.in"
    ;;
  logs)
    docker logs -f simple
    ;;
  test)
    case $2 in
      debug)
        docker exec -ti simple bash -c "PYTEST_DEBUGGER=TRUE DJANGO_SETTINGS_MODULE=simple.settings.test pytest -s"
      ;;
      mon)
        case $3 in
          debug)
            docker exec -ti simple bash -c "PYTEST_DEBUGGER=TRUE DJANGO_SETTINGS_MODULE=simple.settings.test pytest -v --testmon --durations=0"
          ;;
          *)
            docker exec -ti simple bash -c "DJANGO_SETTINGS_MODULE=simple.settings.test pytest -v --testmon --durations=0"
          ;;
        esac
      ;;
      *)
        docker exec -ti simple bash -c "DJANGO_SETTINGS_MODULE=simple.settings.test pytest -n 1 --junitxml=./test-reports/tests.xml"
      ;;
    esac
    ;;
  graph)
    docker exec -ti simple bash -c "./manage.py graph_models -a -g -o ./docs/models.png"
    ;;
  *)
    echo "Unknown command"
    ;;
esac
