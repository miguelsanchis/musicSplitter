build:
    docker build -t music-splitter .

run:
    docker run -p 8000:8000 music-splitter

test:
    pytest

