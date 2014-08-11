PCR_AUTH_TOKEN = 'qL_UuCVxRBUmjWbkCdI554grLjRMPY'

import penncoursereview, json, requests, yaml

DOMAIN = "http://api.penncoursereview.com/v1/"

def generate():
    f = open('profHash', 'w')
    profHash = {}
    r = requests.get(DOMAIN + '/instructors?token=' + PCR_AUTH_TOKEN);
    data = yaml.load(r.text)
    for prof in data["result"]["values"]:
        if profHash.has_key(prof["last_name"]): 
            profHash[prof["last_name"]].append(dict({
                'first_name': prof['first_name'],
                'id': prof['id'],
                'depts': prof['depts']
            }))
        else:
            profHash[prof['last_name']]= [dict({
                'first_name': prof['first_name'],
                'id': prof['id'],
                'depts': prof['depts']
            })]
    print profHash
    f.write(json.dumps(profHash))
    f.close()
generate()