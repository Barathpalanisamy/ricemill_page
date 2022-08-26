import frappe
from frappe.utils import time_diff_in_hours
class classcheck:
    def __init__(self, check):
        self.check1=0
        self.check2=0


@frappe.whitelist()
def setup(ricemill):
    html=''
    if frappe.db.exists("Item", ricemill):
        bom=frappe.get_doc("BOM",{"Item":ricemill})
        html = f'''
            <div id ="initialize">
                <div> 
                    <form action=#>
                        <label for="bom_name">BOM No</label><br>
                        <input type="text" id="bom_name"  value="{bom.name}"><br>
                    </form>
                </div>
                <div>
                    <form action=#>
                        <label for="quantity">Quantity</label><br>
                        <input type="text" id="qty" required><br><br>
                        <input type="submit" id="start_button" value="Start" class="button" onclick="myFunction('{ricemill}')">
                      </form>
                </div>
            </div>
            '''
    return html+css_html()+script()

@frappe.whitelist()
def function(workorder):
    function=f'''
                    <div id="multi-step-form-container">
                           {operation_tracking(workorder)}
                    </div>
    '''
    return function+css_html()
def classname(status,check):
    classlist= {"Open":"form-stepper-unfinished","first_open":"form-stepper-active","Completed":"form-stepper-completed"}
    classname=""
    if(status=="Completed"):
        classname=classlist[status]

    elif(status=="Open" and check.check1==0 ):
        classname=classlist["first_open"]
        check.check1=1
    elif(status=="Open"):
        classname=classlist[status]
    return classname


def operation_tracking(workorder):
    check=classcheck(0)
    
    operation_tracking='''
                <div>   
                   <div id="multi-step-form-container">
                       <!-- Form Steps / Progress Bar -->
                       <ul class="form-stepper form-stepper-horizontal text-center mx-auto pl-0">'''

    work_order=frappe.get_all("Job Card",{"work_order":workorder},["operation","name","status"], order_by = "name")
    if work_order:
        
        operation_tracking +=f'''
                    { "".join([f"""
                    <li class=" {classname(work_order[row].status,check)} text-center form-stepper-list" step="{row+1}">
                        <a class="mx-2">
                            <span class="form-stepper-circle">
                                <span>{row+1}</span>
                            </span>
                            <div class="label">
                                {work_order[row].operation}
                            </div>
                        </a>
                    </li>""" for row in range(len(work_order))])
                    }    
                '''
    return operation_tracking+'</ul></div></div>'+fields_list(work_order)+css_html()+script()


def fields_list(work_order):
    fields_list=' <form id="userAccountSetupForm" name="userAccountSetupForm" enctype="multipart/form-data" method="POST">'
    for row in range(len(work_order)):
        fields_list+=f'''
               
                    <section id="step-{row+1}" class="form-step {"d-none" if(row != 0) else ""}">
                        <h2 class="font-normal">{work_order[row].operation}</h2>
                            {job_card_cus_field()}

                        <div class="mt-3">
                            {f"""<button class="button btn-navigate-form-step" type="button"  jobcard="{work_order[row].name}" step_number="{row+2}">Next</button>""" if(row+1 != len(work_order)) else ""}
                            {f"""<button class="button submit-btn" i onclick="finish()" jobcard="{work_order[row].name}" type="submit">Finish</button>""" if(row+1 == len(work_order)) else ""}
                        </div>
                    </section>  
                '''
    return fields_list + "</form>"

def job_card_cus_field():
    cus_field=f'''
    <div>
          <form >
                    <label for="from_time">From Time</label><br>
                    <input type="datetime-local" id="from_time"><br>
                    <label for="to_time">To Time</label><br>
                    <input type="datetime-local" id="to_time"><br>
                    <label for="total_hrs">Completed Quantity</label><br>
                    <input type="text" id="total_time"><br>
            </form>
    </div>
    '''
    return cus_field


def css_html():
    css_html='''
            <style>
            h1 {
                    text-align: center;
                    }
                    h2 {
                        margin: 0;
                    }
                    #multi-step-form-container {
                        margin-top: 5rem;
                    }
                    .text-center {
                        text-align: center;
                    }
                    .mx-auto {
                        margin-left: auto;
                        margin-right: auto;
                    }
                    .pl-0 {
                        padding-left: 0;
                    }
                    .button {
                        padding: 0.7rem 1.5rem;
                        border: 1px solid #4361ee;
                        background-color: #4361ee;
                        color: #fff;
                        border-radius: 5px;
                        cursor: pointer;
                    }
                    .submit-btn {
                        border: 1px solid #0e9594;
                        background-color: #0e9594;
                    }
                    .mt-3 {
                        margin-top: 2rem;
                    }
                    .d-none {
                        display: none;
                    }
                    .form-step {
                        border: 1px solid rgba(0, 0, 0, 0.1);
                        border-radius: 20px;
                        padding: 3rem;
                    }
                    .font-normal {
                        font-weight: normal;
                    }
                    ul.form-stepper {
                        counter-reset: section;
                        margin-bottom: 3rem;
                    }
                    ul.form-stepper .form-stepper-circle {
                        position: relative;
                    }
                    ul.form-stepper .form-stepper-circle span {
                        position: absolute;
                        top: 50%;
                        left: 50%;
                        transform: translateY(-50%) translateX(-50%);
                    }
                    .form-stepper-horizontal {
                        position: relative;
                        display: -webkit-box;
                        display: -ms-flexbox;
                        display: flex;
                        -webkit-box-pack: justify;
                        -ms-flex-pack: justify;
                        justify-content: space-between;
                    }
                    ul.form-stepper > li:not(:last-of-type) {
                        margin-bottom: 0.625rem;
                        -webkit-transition: margin-bottom 0.4s;
                        -o-transition: margin-bottom 0.4s;
                        transition: margin-bottom 0.4s;
                    }
                    .form-stepper-horizontal > li:not(:last-of-type) {
                        margin-bottom: 0 !important;
                    }
                    .form-stepper-horizontal li {
                        position: relative;
                        display: -webkit-box;
                        display: -ms-flexbox;
                        display: flex;
                        -webkit-box-flex: 1;
                        -ms-flex: 1;
                        flex: 1;
                        -webkit-box-align: start;
                        -ms-flex-align: start;
                        align-items: start;
                        -webkit-transition: 0.5s;
                        transition: 0.5s;
                    }
                    .form-stepper-horizontal li:not(:last-child):after {
                        position: relative;
                        -webkit-box-flex: 1;
                        -ms-flex: 1;
                        flex: 1;
                        height: 1px;
                        content: "";
                        top: 32%;
                    }
                    .form-stepper-horizontal li:after {
                        background-color: #dee2e6;
                    }
                    .form-stepper-horizontal li.form-stepper-completed:after {
                        background-color: #4da3ff;
                    }
                    .form-stepper-horizontal li:last-child {
                        flex: unset;
                    }
                    ul.form-stepper li a .form-stepper-circle {
                        display: inline-block;
                        width: 40px;
                        height: 40px;
                        margin-right: 0;
                        line-height: 1.7rem;
                        text-align: center;
                        background: rgba(0, 0, 0, 0.38);
                        border-radius: 50%;
                    }
                    .form-stepper .form-stepper-active .form-stepper-circle {
                        background-color: #4361ee !important;
                        color: #fff;
                    }
                    .form-stepper .form-stepper-active .label {
                        color: #4361ee !important;
                    }
                    .form-stepper .form-stepper-active .form-stepper-circle:hover {
                        background-color: #4361ee !important;
                        color: #fff !important;
                    }
                    .form-stepper .form-stepper-unfinished .form-stepper-circle {
                        background-color: #f8f7ff;
                    }
                    .form-stepper .form-stepper-completed .form-stepper-circle {
                        background-color: #0e9594 !important;
                        color: #fff;
                    }
                    .form-stepper .form-stepper-completed .label {
                        color: #0e9594 !important;
                    }
                    .form-stepper .form-stepper-completed .form-stepper-circle:hover {
                        background-color: #0e9594 !important;
                        color: #fff !important;
                    }
                    .form-stepper .form-stepper-active span.text-muted {
                        color: #fff !important;
                    }
                    .form-stepper .form-stepper-completed span.text-muted {
                        color: #fff !important;
                    }
                    .form-stepper .label {
                        font-size: 1rem;
                        margin-top: 0.5rem;
                    }
                    .form-stepper a {
                        cursor: default;
                    }
                    </style>

    '''
    return css_html

def script():
    script='''  
    <script>
            let navigateToFormStep = async (stepNumber,idclass) => {

                    var fromtime=document.getElementById("from_time").value;
                    var totime=document.getElementById("to_time").value;
                    var totalhrs=document.getElementById("total_time").value;
                
                    if(fromtime && totime &&totalhrs){
                      await  frappe.call({
                            method:"retail.retail.page.manufacturing_rice.work_order.jobcard_creation",
                            args:{fromtime:fromtime,totime:totime,totalhrs:totalhrs, jobname:idclass},
                        })
                     frappe.show_alert({
                            message:__('Job Card Submitted'),
                            indicator:'green'
                        });
                    }
                    else {
                        frappe.show_alert({
                            message:__('Value is missing'),
                            indicator:'red'
                        });
                        return 
                    }

                document.querySelectorAll(".form-step").forEach((formStepElement) => {
                    formStepElement.classList.add("d-none");
                });
                console.log("xvsgcgs")
                document.querySelectorAll(".form-stepper-list").forEach((formStepHeader) => {
                    formStepHeader.classList.add("form-stepper-unfinished");
                    formStepHeader.classList.remove("form-stepper-active", "form-stepper-completed");
                });
                document.querySelector("#step-" + stepNumber).classList.remove("d-none");
                
                let formStepCircle = document.querySelector('li[step="' + stepNumber + '"]');
                formStepCircle.classList.remove("form-stepper-unfinished", "form-stepper-completed");
                formStepCircle.classList.add("form-stepper-active");  
                for (let index = 0; index < stepNumber; index++) {     
                    let formStepCircle = document.querySelector('li[step="' + index + '"]');     
                    if (formStepCircle) {
                        formStepCircle.classList.remove("form-stepper-unfinished", "form-stepper-active");
                        formStepCircle.classList.add("form-stepper-completed");
                    }
                }
            };


            document.querySelectorAll(".btn-navigate-form-step").forEach((formNavigationBtn) => {
                formNavigationBtn.addEventListener("click", () => {
                    let stepNumber = parseInt(formNavigationBtn.getAttribute("step_number"));
                    let idclass = formNavigationBtn.getAttribute("jobcard");
                    navigateToFormStep(stepNumber,idclass);
            
                });
            });
        
          
    </script>

    '''
    return script

# def cus_field():
