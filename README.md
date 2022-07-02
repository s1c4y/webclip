![build-badge](https://github.com/s1c4y/webclip/workflows/build/badge.svg?branch=main)
<br>
# WebClip

simple file and textsharing in local networks 
<br><br>
upload a file with curl: <code>curl -F "file=@myfile.bin" http://0.0.0.0/upload</code> <br>
download a file with curl: <code>curl http://0.0.0.0/dl/myfile.bin -o myfile.bin</code>

## Using Docker
```
docker run --name webclip --restart unless-stopped -p 8080:5000 s1c4y/webclip:latest
```
