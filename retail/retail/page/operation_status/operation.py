import frappe
from frappe.utils import time_diff_in_hours

@frappe.whitelist()
def setup(work_order):
    html=""

    if frappe.db.exists("Work Order", work_order):
        workorder=frappe.get_doc("Work Order",work_order)

        if workorder.operations:
            for i in workorder.operations:
                html += f'''
                    <head>
                        <link rel="preconnect" href="https://fonts.googleapis.com">
                        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
                        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@200&display=swap" rel="stylesheet">
                    </head>
  
                    <div class='div1'>
                        <div class='htmlinfo'> 
                           Operation Name :<br>
                            {i.operation}
                        </div>
                        <div class='htmlinfo'>
                            <b>Start Date & Time</b> : {str(workorder.actual_start_date).split(".")[0]}<br>
                            End Date & Time : {str(workorder.actual_end_date).split(".")[0]} <br>
                           <b>Total Hours</b> : {(time_diff_in_hours(workorder.actual_end_date,workorder.actual_start_date)):.2f}<br>
                        </div>
                        <div class='htmlinfo1'>
                           Job Card Details <br>
                           {job_card(workorder)}
                        </div>
                    </div>
                    '''
            return item_manufacture(workorder)+html+html_style()


def item_manufacture(workorder):
    item_html=f''' 
            <div class='div'>
                <div class='htmlinfos'>
                    Item Name : {workorder.item_name}<br>
                    <img src="{frappe.db.get_value('Item',workorder.production_item,'image')}" alt="{workorder.production_item}" width="150" height="150">
                </div>
                <div class='htmlinfos'>
                    Qty To Manufacture : {workorder.qty}
                </div>
                <div class='htmlinfos1'>
                    Manufactured Qty : {workorder.produced_qty}
                </div>
            </div>
    '''
    return item_html

def job_card(workorder):
    status=["Open","Work In Progress","Completed"]
    jobcard_status= ""
    for j in status:
        jobcard_status+=f'''{j} : {len(frappe.get_all("Job Card",filters={"work_order":workorder.name,"Status":j}))}<br> '''
    return jobcard_status
    


def html_style():
    style = '''
            <style>
                .htmlinfo{
                float:left;
                width:30%;
                color:#5F4B8BFF;
                font-family: 'Poppins', sans-serif;
            }
                .htmlinfo1{
                float:right;
                width:30%;
                color:#5F4B8BFF;
                font-family: 'Poppins', sans-serif;
            }
            .htmlinfos{

                float:left;
                width:30%;
                color:#E69A8DFF;
                font-family: 'Poppins', sans-serif;

            }
            .htmlinfos1{

                float:right;
                width:30%;
                color:#E69A8DFF;
                font-family: 'Poppins', sans-serif;

            }
            .div{
                background-color:#5F4B8BFF;
                color:white;
                font-weight:bold;
                border-radius:10px;
                height:178px;
                width:100%;
                margin-bottom:5px;
                padding:20px;
                font-size:17px;
                line-height:2;
            }
            .div1{
                background-color:#E69A8DFF;
                color:white;
                font-weight:bold;
                border-radius:10px;
                height:178px;
                width:100%;
                margin-bottom:5px;
                padding:20px;
                font-size:17px;
                line-height:2;
            }
           
            
        .button {
                font-size: 15px;
                text-align: center;
                margin-left:5px;
                color: #fff;
                background-color: #FDD037;
                border: none;
                border-radius: 5px;
                border-style: none;
                outline:none;

                }
            .button:focus{outline:none;}
            .button:active{font-size:16px;
                    margin-left:7px;
                }
            
            </style>
        '''
    return style