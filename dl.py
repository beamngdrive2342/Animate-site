import urllib.request
import certifi
import ssl

context = ssl.create_default_context(cafile=certifi.where())

urls = [
    ("cdece41ffcb74a918d41d6bde21779ba", "https://contribution.usercontent.google.com/download?c=CgthaWRhX2NvZGVmeBJ7Eh1hcHBfY29tcGFuaW9uX2dlbmVyYXRlZF9maWxlcxpaCiVodG1sXzUxZGI1ZWVkYTJmZjQ3YjdiY2UwYTcwOTQwMGE0NTVmEgsSBxDg1rXlhhQYAZIBIwoKcHJvamVjdF9pZBIVQhM1MzYwODY4NzI4NTUxNTI0NDI1&filename=&opi=96797242"),
    ("93fce9eccd3d40cab4787685ecd86d75", "https://contribution.usercontent.google.com/download?c=CgthaWRhX2NvZGVmeBJ7Eh1hcHBfY29tcGFuaW9uX2dlbmVyYXRlZF9maWxlcxpaCiVodG1sX2I3MGJmZDNiMWQ5ODRkNjhhOTNiYTkxY2ZiN2JmYzg1EgsSBxDg1rXlhhQYAZIBIwoKcHJvamVjdF9pZBIVQhM1MzYwODY4NzI4NTUxNTI0NDI1&filename=&opi=96797242"),
    ("24237488251b4a45b06da75ac321d214", "https://contribution.usercontent.google.com/download?c=CgthaWRhX2NvZGVmeBJ7Eh1hcHBfY29tcGFuaW9uX2dlbmVyYXRlZF9maWxlcxpaCiVodG1sX2U2NDY5M2U0M2IxZjRkY2I4MTczMTVlMTRhZGQ5NjhlEgsSBxDg1rXlhhQYAZIBIwoKcHJvamVjdF9pZBIVQhM1MzYwODY4NzI4NTUxNTI0NDI1&filename=&opi=96797242"),
    ("9f304bf6e2ea4cdc863c8ec3afd5cbff", "https://contribution.usercontent.google.com/download?c=CgthaWRhX2NvZGVmeBJ7Eh1hcHBfY29tcGFuaW9uX2dlbmVyYXRlZF9maWxlcxpaCiVodG1sXzViNDJiMjFkOWQyODQxNjU4N2Y2MGVkNDA1MjM4MzcxEgsSBxDg1rXlhhQYAZIBIwoKcHJvamVjdF9pZBIVQhM1MzYwODY4NzI4NTUxNTI0NDI1&filename=&opi=96797242"),
    ("b64885b5a98543e6a57c92c1acd5d90e", "https://contribution.usercontent.google.com/download?c=CgthaWRhX2NvZGVmeBJ7Eh1hcHBfY29tcGFuaW9uX2dlbmVyYXRlZF9maWxlcxpaCiVodG1sX2Q1N2I3MWRhYWJkYzQ3NzRhNDk4ZWNmOTg5NTViZWQ4EgsSBxDg1rXlhhQYAZIBIwoKcHJvamVjdF9pZBIVQhM1MzYwODY4NzI4NTUxNTI0NDI1&filename=&opi=96797242")
]

for name, url in urls:
    print(f"Downloading {name}...")
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    try:
        with urllib.request.urlopen(req, context=context) as response:
            html = response.read().decode('utf-8')
            with open(f"screen_{name}.html", "w", encoding='utf-8') as f:
                f.write(html)
    except Exception as e:
        print(f"Error {name}: {e}")
