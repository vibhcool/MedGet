import infermedica_api

infermedica_api.configure(app_id='Your App Id', app_key='App Key')

class medget:

    api = infermedica_api.get_api()

    def get_data(self,sex_m,age_m):
    ''' Initialize the user to be diagnosed
    '''
        self.user_data = infermedica_api.Diagnosis(sex=sex_m.lower(), age=age_m)
        
    
    def add_symptoms(self, ids):
    ''' The ids is the list of dicts with keys 'id' and 'status' 
    '''    
        for i in ids:
            self.user_data.add_symptom( 
                str(i[str(u'id')]),
                str(i[str(u'status')])
            )
        
    def search_symptoms(self, symptoms_str):
    ''' Outputs more symptoms related to symptom_str (is a list of symptoms)
        user enters
    '''
        search_res = []
        for i in symptoms_str:
            res = self.api.search(i)

            for k in res:
                res_p = {}
                res_p['id'] = str(k[str('id')])
                res_p['label'] = str(k[str('label')])
                search_res.append(res_p)
                res_p=None
        return search_res

    def get_question(self, ):
    ''' Diagnose the previous question/symptoms input 
        and gives the next question
    '''
        self.user_data = self.api.diagnosis(self.user_data)
        optn_list = []
        ques = {}
        ques['text'] = self.user_data.question.text
        ques['option'] = []

        for i in self.user_data.question.items:
            optn = {}
            optn['id'] = i['id']
            optn['name'] = i['name']
            optn['choice'] = i['choices']

            ques['option'].append(optn)
        return ques
        
    def check_risk(self, risk_prob=0.7):
    ''' Outputs the risk of disease the user may have according
        to the probability risk_prob 
    '''
        if self.user_data.conditions[0]['probability'] > risk_prob:
            return 1
        else:
            return 0

    def get_result(self, ):
    ''' Outputs the probable disease the user may have
    '''
        result = {}
        result['id'] = str(self.user_data.conditions[0][str('id')])      
        result['name'] = str(self.user_data.conditions[0][str('name')])
        result['prob'] = str(self.user_data.conditions[0]['probability'])
        k = self.api.condition_details(result['id']).__dict__
        result['hint'] = str(k[str('extras')][str('hint')])
        result['severity'] = str(k[str('severity')])
        result['prevalence'] = str(k[str('prevalence')])
        result['acuteness'] = str(k[str('acuteness')])
        return result

