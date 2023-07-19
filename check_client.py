# -*- coding: UTF-8 -*-

# Author   : Jason Hung
# Build    : 20230712
# update   : 20230713
# Function : check card reader client status in windows

import psutil , smtplib , requests , logging , time , pymysql


#####################################################################################
#
# variables
#
#####################################################################################
db = {'host':'192.168.1.93' , 'port':3306 , 'user' : 'otsuka', 'pwd':'OtsukatW168!' , 'db':'otsuka_invoice_history' , 'charset':'utf8'}

#####################################################################################
#
# class - check_card_reader
#
#####################################################################################
class check_card_reader:
    
    ############
    # logging
    ############
    logging.basicConfig(level=logging.INFO , format="%(asctime)s %(message)s " , datefmt="%Y-%m-%d %H:%M:%S")

    #########
    # init
    #########
    def __init__(self):
        try:
            ###　card reader - taipei
            taipei_card_reader_client = 'client.exe'
            
            ### test 
            #self.check_process_status(taipei_card_reader_client)
            
            while True:
                
                self.check_process_status(taipei_card_reader_client)
                    
                time.sleep(300)

        except Exception as e:
            logging.info('< Error > init : ' + str(e))
        finally:
            pass
    
    #######################
    # check_db_record
    #######################
    def save_db_record(self , status , cpu):
        conn = pymysql.connect(host=db['host'],port=db['port'],user=db['user'],passwd=db['pwd'],database=db['db'],charset=db['charset'])    
        curr = conn.cursor()

        try:
            ### time record
            now_day = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime()) 
            r_date  = time.strftime("%Y-%m-%d" , time.localtime()) 
            r_time  = time.strftime("%H:%M:%S" , time.localtime()) 

            #check_sql = "select c_date from check_record where c_date='{0}'".format(now_day)
            #curr.execute(check_sql)
            #res = curr.fetchone()
        
            # if res is None:
            if status == 'success':
                sql = "insert into success_record(c_date , r_date , r_time , content , cpu) value('{0}','{1}','{2}','{3}','{4}')".format(now_day , r_date , r_time , '701Client 連線中' , cpu)
            elif status == 'fail':
                sql = "insert into fail_record(c_date , r_date , r_time , content , cpu) value('{0}','{1}','{2}','{3}','{4}')".format(now_day , r_date , r_time , '701Client 斷線' , cpu)

            curr.execute(sql)
            conn.commit()

        except Exception as e:
            logging.info('< Error > save_db_record : ' + str(e))

        finally:
            conn.close()

    ########################
    # success_record_file
    ########################
    def success_record_file(self,record_txt):
        try:
            ### time record
            now_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime()) 

            #########################  
            # save success to file
            #########################
            file = open("success_record.txt" , "a")    
            r_txt = now_time + " " + record_txt
            file.write(r_txt)
            file.close()

            ###########################
            # save success db record
            ###########################
            data = record_txt.split(',')
            cpu = data[1]
            self.save_db_record('success' , cpu)

        except Exception as e :
            logging.info('< Error > success_record_file :' + str(e))
        finally:
            pass

    #####################
    # fail_record_file
    #####################
    def fail_record_file(self,record_txt):
        try:
            # time record
            now_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime()) 
            
            ######################
            # save fail to file
            ######################
            file = open("fail_record.txt" , "a")    
            r_txt = now_time + " " + record_txt
            file.write(r_txt)
            file.close()

            ########################
            # save fail db record
            ########################
            data = record_txt.split(',')
            cpu = data[1]
            self.save_db_record('fail' , cpu)


        except Exception as e :
            logging.info('< Error > fail_record_file : ' + str(e))
        finally:
            pass

    ################
    # line_notify
    ################
    def line_notify(self, cpu_percent):
        
        try:
            ### 1 by 1
            token = 'G2caVYeO1TmbabvCu2j7sUMmaMLmrhlwt8YSW25tMWA'
            
            ### 1 by many
            token2 = 'sBXL6uZvu6qLoWQOXisF79Qd7XPhko91Ley5MCKyt2Q'
            
            msg = '台北 刷卡機 - 701client 斷線 , cpu ' + str(cpu_percent) + ' %'
            
            headers = {
                "Authorization" : "Bearer " + token2 , 
                "Content-Type" : "application/x-www-form-urlencoded"
            }

            payload = {'message' : msg}
            r = requests.post("https://notify-api.line.me/api/notify" , headers=headers , data=payload) 
            
            ### fail record file
            if r.status_code == 200:
                self.fail_record_file(msg+"\n")
        
        except Exception as e:
            logging.info('< Error > line_notify : ' + str(e))
        finally:
            pass

    
    ################
    # line_notify2
    ################
    def line_notify2(self, msg):
        
        try:
            # time record
            now_time  = time.strftime("%Y-%m-%d %H:%M:%S" , time.localtime()) 
            
            # 1 by 1
            token = 'G2caVYeO1TmbabvCu2j7sUMmaMLmrhlwt8YSW25tMWA'
            
            # 1 by many
            token2 = 'sBXL6uZvu6qLoWQOXisF79Qd7XPhko91Ley5MCKyt2Q'
            
            msg = '\n' + now_time + ' , ' + msg + '\n'
            
            headers = {
                "Authorization" : "Bearer " + token2 , 
                "Content-Type" : "application/x-www-form-urlencoded"
            }

            payload = {'message' : msg}
            r = requests.post("https://notify-api.line.me/api/notify" , headers=headers , data=payload) 
            
            ### fail record file
            if r.status_code == 200:
                self.fail_record_file(msg+"\n")

                ########################
                # save fail db record
                ########################
                self.save_db_record('fail' , '0')
        
        except Exception as e:
            logging.info('< Error > line_notify : ' + str(e))
        finally:
            pass

    #########################
    # check_process_status
    #########################
    def check_process_status(self,process_name):
        try:
            for process in psutil.process_iter():
                
                if process.name() == process_name and process.status() == 'running':
                
                    ### if 701client cpu used over 80 % is process crash.
                    if process.cpu_percent(interval=1) < 80:
                        logging.info("台北 刷卡機 - 701client 連線中 , cpu : " + str(process.cpu_percent(interval=1)) + ' %')
                        
                        ### success record file
                        self.success_record_file("台北 刷卡機 - 701client 連線中 , cpu : " + str(process.cpu_percent(interval=1)) + " %\n")

                        return True
                    else:
                        logging.info("台北 刷卡機 - 701client 斷線 , cpu : " +  str(process.cpu_percent(interval=1)) + ' %')
                        
                        ### line notify
                        self.line_notify(process.cpu_percent(interval=1))
                        
                        return False
                    
            ### line notify2 程式未啟動
            msg = '\n' + '台北 刷卡機 701client , 程式未啟動 !\n'
            self.line_notify2(msg)
            return False
                            
        except Exception as e:
            logging.info('< Error > check_process_status : ' + str(e))
        finally:
            pass

    ###############
    # send_email
    ###############
    def send_email(self,resceive_addr):
        try:
            smtp = smtplib.SMTP('smtp.office365.com' , 588)
            smtp.ehlo()
            smtp.starttls()
            smtp.login('Jason_Hung@otsuka','!qaz2wsx3e')
            from_addr = 'Jason_Hung@otsuka.com.tw'
            to_addr = resceive_addr
            msg = "Subject:Otsuka sent by check 701client status from Taipei card reader \n 701client 斷線"
            status = smtp.sendmail(from_addr , to_addr , msg)

            if status =={}:
                logging.info("701client 狀態 : 斷線 , 傳送成功.")
            else:
                logging.info("701client 狀態 : 斷線 , 傳送失敗.")

            smtp.quit()
        except Exception as e:
            logging.info(' <Error> send_email : ' + str(e))
        finally:
            pass

#####################################################################################
#
# main
#
#####################################################################################
if __name__ == '__main__':
    
    ### check taipei card reader client status
    check_taipei_card_reader = check_card_reader()
    
   
        
    
