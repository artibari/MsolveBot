import pymongo
database_json = '/var/www/html/database.json'
answers_json = '/var/www/html/answers.json'
syn_file = '/var/www/html/syn.csv'
con = pymongo.MongoClient('ntech.mahindra.com',27017)
#con = pymongo.MongoClient()
# mongo_path_nestaway_chat_logs = con.nestaway.Log
mongo_path_mlu_lastResp = con.mlu.mluLastResp
mongo_path_mlu_convoLogs = con.mlu.mluConvoLogs
mongo_path_mSolve_lastResp = con.mSolve.mSolveLastResp
mongo_path_mSolve_convoLogs = con.mSolve.mSolveConvoLogs
mongo_path_mSolve_userDetails = con.mSolve.mSolveUserDetails
mongo_path_mandi_lastResp = con.mandi.mandiLastResp
mongo_path_mSolve_ticketDetails = con.mSolve.mSolveTicketDetails
mongo_path_mSolve_ticketArchieve = con.mSolve.mSolveTicketArchieve
mongo_path_mSolve_bmcError = con.mSolve.BMCError
mongo_path_unclassifiedQueries = con.mSolve.unclassifiedQueries
