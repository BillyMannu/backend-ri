from cmath import exp
from distutils.filelist import findall
from logging import exception
# from logging import exception
from flask import Flask, request, make_response
from flask_cors import CORS
from flask_cors import cross_origin
# import json, jsonify
from urllib3 import Retry
from helpers import Penzi
from helpers import Start
from helpers import Details
from helpers import Myself
from helpers import Match
from helpers import Next
from helpers import Choice
from helpers import Chosen
from helpers import Description
from helpers import Accept
from helpers import Deactivate

app = Flask(__name__)
cors = CORS(app)

app.config['CORS_HEADERS'] = 'content-Type'

penzi_class = Penzi()
start_class = Start()
details_class = Details()
myself_class = Myself()
match_class = Match()
next_class = Next()#
choice_class = Choice()#ready>>> joining front end
chosen_class = Chosen()#ready>>> joining front end
description_class = Description()#ready>>> joining front end
accept_class = Accept()# for when one responds with 'YES'   NOT READY
deactivate_class = Deactivate()#Not ready

#API
@app.route("/penzi", methods=['POST','GET'])
@cross_origin()
def messages():
    #Check CODEWORD sent by client
    try:
        data = request.get_json()
        message = data.get('message')
        number = data.get('number')
        
        print(data)
        txt=message.upper()

        
        if txt == 'PENZI':
                        response = penzi_class.penzi(number=number, message=message)
                        return response

        elif txt == 'YES':
                            response = match_class.match(number=number, message=message)
                            return response

            

        elif txt == 'ACTIVATE':
            return response
        


        
        else:

            x = message.split("#")  #Split string received 
            y = x.pop(0)  #select CODEWORD in message( first word )

            txt = y.upper()  #convert CODEWORD to uppercase                

            if txt == 'START':
                response = start_class.start(number=number, message=message)
                return response

            elif txt == 'DETAILS':
                response = details_class.details(number=number, message=message)
                return response

            elif txt == 'MATCH' :
                print(txt)

                response= match_class.match(number=number, message=message)
               
                return response  
            else: 
                x = message.split()[0]  
                txt = x.upper()
                if txt == 'MYSELF':
                    print(txt)

                    response = myself_class.myself(number=number, message=message)
                    return response
                
                  
                elif txt == 'DESCRIBE':                    
                    print(txt)

                    response = description_class.description(number = number,message = message)
                    return response
                    
                else:
                    if message.startswith('07')== True :
                        response = choice_class.choice(number = number,message=message) #Request for more details about a prefered date
                        response1 = chosen_class.chosen(number = number,message=message) # the date whose details have been sought for gets details about interested party
                        
                        return response,response1# sort this out !!!!
                    
                    elif message.startswith('+254')== True :
                        response = choice_class.choice(number = number,message=message) #Request for more details about a prefered date
                        response1 = chosen_class.chosen(number = number,message=message) # the date whose details have been sought for gets details about interested party
                        
                        return response
                    
                    else:
                        return make_response({
                            "message":"You did not send a valid codeword"
                        })
    except exception as e:
        print(e)
        return make_response({
                "message":"Error processing your request"
            })
            


if __name__ == '__main__':
    app.run()# Update host with nginx

