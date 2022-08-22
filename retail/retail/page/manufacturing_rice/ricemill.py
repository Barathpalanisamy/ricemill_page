import frappe
from frappe.utils import time_diff_in_hours
@frappe.whitelist()
def setup(ricemill):
    html=''
    if frappe.db.exists("Item", ricemill):
        bom=frappe.get_doc("BOM",{"Item":ricemill})
        html = f'''
            <div>
                <div'> 
                    <form action=#>
                    <label for="bom_name">BOM No</label><br>
                    <input type="text" id="bom_name"  value="{bom.name}"><br>
                    </form>
                </div>
                <div>
                    <form action=#>
                        <label for="quantity">Quantity</label><br>
                        <input type="text" id="qty"><br>
                    </form>
                </div>
                   <div>
                <form action=#>
                        <button class="button" onclick="myFunction('{ricemill}')">Try it</button>
                    </form>
                </div>
                 <div>    
                    <div id="multi-step-form-container">
                           {operation_tracking(ricemill)}
                    </div>
                <div>
            '''
    return html+css_html()+script()

def operation_tracking(ricemill):
    operation_tracking='''
                <div>   
                   <div id="multi-step-form-container">
                       <!-- Form Steps / Progress Bar -->
                       <ul class="form-stepper form-stepper-horizontal text-center mx-auto pl-0">'''
    work_order=frappe.get_doc("BOM",{"Item":ricemill})
    if work_order.operations:
        operation_tracking +=f'''
                    { "".join([f"""
                    <li class="{"form-stepper-active" if(row == 0) else "form-stepper-unfinished"} text-center form-stepper-list" step="{row+1}">
                        <a class="mx-2">
                            <span class="form-stepper-circle {"text-muted" if(row>0) else ""}">
                                <span>{row+1}</span>
                            </span>
                            <div class="label">
                                {work_order.operations[row].operation}
                            </div>
                        </a>
                    </li>""" for row in range(len(work_order.operations))])
                    
                    }
                    
                '''
    return operation_tracking+'</ul></div></div>'+fields_list(work_order)

def fields_list(work_order):
    fields_list=' <form id="userAccountSetupForm" name="userAccountSetupForm" enctype="multipart/form-data" method="POST">'
    for row in range(len(work_order.operations)):
        fields_list+=f'''
               
                    <section id="step-{row+1}" class="form-step {"d-none" if(row != 0) else ""}">
                        <h2 class="font-normal">{work_order.operations[row].operation}</h2>
                        <div class="mt-3">
                        </div>
                        <div class="mt-3">
                            {f"""<button class="button btn-navigate-form-step" type="button" step_number="{row+2}">Next</button>""" if(row+1 != len(work_order.operations)) else ""}
                            {"""<button class="button submit-btn" type="submit">Finish</button>""" if(row+1 == len(work_order.operations)) else ""}
                        </div>
                    </section>     
                

                '''
    return fields_list + "</form>"

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
        function myFunction(ricemill) {

           var a= document.getElementById("qty").value;
           var b= document.getElementById("bom_name").value;
            frappe.call({
                    method: "retail.retail.page.manufacturing_rice.work_order.work_order_creation",
                    args:{a:a,b:b, c:ricemill},
                    
                });
            }
         


            const navigateToFormStep = (stepNumber) => {
                document.querySelectorAll(".form-step").forEach((formStepElement) => {
                    formStepElement.classList.add("d-none");
                });
                
                document.querySelectorAll(".form-stepper-list").forEach((formStepHeader) => {
                    formStepHeader.classList.add("form-stepper-unfinished");
                    formStepHeader.classList.remove("form-stepper-active", "form-stepper-completed");
                });
                document.querySelector("#step-" + stepNumber).classList.remove("d-none");
                const formStepCircle = document.querySelector('li[step="' + stepNumber + '"]');
                formStepCircle.classList.remove("form-stepper-unfinished", "form-stepper-completed");
                formStepCircle.classList.add("form-stepper-active");  
                for (let index = 0; index < stepNumber; index++) {     
                    const formStepCircle = document.querySelector('li[step="' + index + '"]');     
                    if (formStepCircle) {
                        formStepCircle.classList.remove("form-stepper-unfinished", "form-stepper-active");
                        formStepCircle.classList.add("form-stepper-completed");
                    }
                }
            };

            document.querySelectorAll(".btn-navigate-form-step").forEach((formNavigationBtn) => {
                formNavigationBtn.addEventListener("click", () => {
                    const stepNumber = parseInt(formNavigationBtn.getAttribute("step_number"));
                    navigateToFormStep(stepNumber);
                });
            });

    </script>

    '''
    return script