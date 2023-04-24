# Hit counter

### Start (in localhost)

Clone repository

```bash
git clone git@github.com:da-tot-samy-ilya/hit_counter.git hit_counter
```

Change dir

```bash
cd hit_counter
```

Start app

```bash
python server.py
```
### Description

This server in Flask can count visits on any site using cookies. Also it can give statistics by days, month, years and all time.

### Get statistics:
1. Unique visitors for all time<br>
<http://127.0.0.1:5000/api/counter/unique/all>

2. Unique visitors for exactly date<br>
<http://127.0.0.1:5000/api/counter/unique/2023/04/24><br>
<http://127.0.0.1:5000/api/counter/unique/2023/04><br>
<http://127.0.0.1:5000/api/counter/unique/2023>
3. Not unique visitors for all time<br>
<http://127.0.0.1:5000/api/counter/not_unique/all>
4. Not unique visitors for exactly date<br>
<http://127.0.0.1:5000/api/counter/not_unique/2023/04/24><br>
<http://127.0.0.1:5000/api/counter/not_unique/2023/04><br>
<http://127.0.0.1:5000/api/counter/not_unique/2023>