import sys,time,requests
c=input("Cookie: ").strip()
s=requests.Session();s.cookies['.ROBLOSECURITY']=c
r=s.post("https://auth.roblox.com/v2/login")
t=r.headers.get("X-CSRF-TOKEN")or exit("[!] No CSRF")
s.headers['X-CSRF-TOKEN']=t
u=s.get("https://users.roblox.com/v1/users/authenticated").json()
print(f"[+] {u['name']}")
f=s.get(f"https://friends.roblox.com/v1/users/{u['id']}/friends").json()['data']
if not f:exit("[!] No friends")
print(f"[*] {len(f)} friends")
if input("Delete all? (y/n): ").lower()!='y':exit()
d=0
for p in f:
 for a in range(3):
  r=s.post(f"https://friends.roblox.com/v1/users/{p['id']}/unfriend")
  if r.status_code==200:d+=1;print(f"✓ {p['name']}");break
  if r.status_code==429:time.sleep(5*(a+1))
  if r.status_code==403 and (t:=r.headers.get("X-CSRF-TOKEN")):s.headers['X-CSRF-TOKEN']=t;continue
  time.sleep(3)
 time.sleep(0.6)
print(f"[+] Done: {d}/{len(f)}")
