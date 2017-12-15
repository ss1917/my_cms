```
upstream  mg{
    server  127.0.0.1:9000;
    server  127.0.0.1:9001;
    server  127.0.0.1:9002;
}

upstream  task{
    server  127.0.0.1:9100;
    server  127.0.0.1:9101;
    server  127.0.0.1:9102;
}


server
{
        listen 80;
        server_name cms.test.com;
        access_log /var/log/nginx/cms_access.log;
        error_log  /var/log/nginx/cms_error.log;
        index index.html index.htm;
        root  /home/dev/python_dev/my_cms;
        server_name_in_redirect  off;
        access_log  off;
        # Allow file uploads
        client_max_body_size 20M;
        proxy_read_timeout 10;

        location = /favicon.ico {
            rewrite (.*) /static/favicon.ico;
        }

        location ^~ /static/ {
                    alias /home/dev/python_dev/my_cms/static/;
                    if ($query_string) {
                        expires max;
                    }
                }

        location ^~ /common/ {
                    alias /home/dev/python_dev/my_cms/static/common/;
                    if ($query_string) {
                        expires max;
                    }
                }

        location ^~ /backstage/ {
                    alias /home/dev/python_dev/my_cms/static/backstage/;
                    if ($query_string) {
                        expires max;
                    }
                }

        location / {
                proxy_pass_header cms.test.com;
                proxy_set_header Host $http_host;
                proxy_redirect off;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Scheme $scheme;
                proxy_pass http://mg;
        }

        location /v1/task/ {
                proxy_pass_header cms.test.com;
                proxy_set_header Host $http_host;
                proxy_redirect off;
                proxy_set_header X-Real-IP $remote_addr;
                proxy_set_header X-Scheme $scheme;
                proxy_pass http://task;
        }

}
```