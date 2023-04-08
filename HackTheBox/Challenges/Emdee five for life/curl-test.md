# Curl Test
## Details of the curl commands and server responses.

### First GET Request
```bash
curl {IP Address}:{Port}
<html>
<head>
<title>emdee five for life</title>
</head>
<body style="background-color:powderblue;">
<h1 align='center'>MD5 encrypt this string</h1><h3 align='center'>p9kAsudKVh3UVEDJurGS</h3><center><form action="" method="post">
<input type="text" name="hash" placeholder="MD5" align='center'></input>
</br>
<input type="submit" value="Submit"></input>
</form></center>
</body>
</html>
```
### POST Request, without cookie
```bash
curl --data "hash":"beea6b41ab3a4cf8b875c184b9c7f147" {IP Address}:{Port}}
<html>
<head>
<title>emdee five for life</title>
</head>
<body style="background-color:powderblue;">
<h1 align='center'>MD5 encrypt this string</h1><h3 align='center'>EkKslzkYQhPVkS2DloFK</h3><center><form action="" method="post">
<input type="text" name="hash" placeholder="MD5" align='center'></input>
</br>
<input type="submit" value="Submit"></input>
</form></center>
</body>
</html>
```
### POST Request, with cookie
```bash
curl --data "hash=f726c4a8818b8dc67f8ce26e3b45ba77" --cookie "PHPSESSID={Session ID}" {IP Address}:{Port} 
<html>
<head>
<title>emdee five for life</title>
</head>
<body style="background-color:powderblue;">
<h1 align='center'>MD5 encrypt this string</h1><h3 align='center'>HKRAE8lUpxCamQitBsh8</h3><p align='center'>Too slow!</p><center><form action="" method="post">
<input type="text" name="hash" placeholder="MD5" align='center'></input>
</br>
<input type="submit" value="Submit"></input>
</form></center>
</body>
</html>
```