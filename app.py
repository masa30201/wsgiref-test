import os
from wsgiref.simple_server import make_server
from urllib.parse import parse_qs

def app(environ, start_response):
    if environ.get("PATH_INFO", "/") == "/" and environ["REQUEST_METHOD"] in ("GET", "POST"):
        if environ["REQUEST_METHOD"] == "POST":
            size = int(environ.get("CONTENT_LENGTH") or 0)
            data = environ["wsgi.input"].read(size).decode()
            q = parse_qs(data)
        else:
            q = parse_qs(environ.get("QUERY_STRING", ""))

        try:
            a = float(q.get("a", ["0"])[0])
            b = float(q.get("b", ["0"])[0])
        except ValueError:
            a, b = 0.0, 0.0

        body = f"""<!doctype html><meta charset="utf-8">
        <h1>足し算</h1>
        <form method="post">
          <input name="a" type="number" step="any" value="{a}"> +
          <input name="b" type="number" step="any" value="{b}">
          <button>=</button>
        </form>
        <p>結果: <strong>{a+b}</strong></p>""".encode("utf-8")

        start_response("200 OK", [("Content-Type", "text/html; charset=utf-8")])
        return [body]

    start_response("404 Not Found", [("Content-Type", "text/plain; charset=utf-8")])
    return [b"Not found"]

if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    # ← クラウドで必須（外部からアクセス可能に）
    with make_server("0.0.0.0", port, app) as httpd:
        httpd.serve_forever()
