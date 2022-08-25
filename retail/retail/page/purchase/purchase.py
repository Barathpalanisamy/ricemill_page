import frappe
import json
from erpnext.selling.page.point_of_sale.point_of_sale import search_for_serial_or_batch_or_barcode_number as barcode
@frappe.whitelist()
def setup(item_list):
        item_list = json.loads(item_list)
        html = f'''
            <table id="table">
                <tr><th></th>
                    <th>Item </th>
                    <th>Rate</th>
                    <th>Item </th>
                    <th>Rate</th> 
                    <th>Item </th>
                    <th>Rate</th>
                    <th>Item </th>
                    <th>Rate</th>
                    <th>Item </th>
                    <th>Rate</th>
                    <th>Item </th>
                    <th>Rate</th>
                    <th>Rate</th>
                    <th>Item </th>
                    <th>Rate</th>
                </tr>
                {table_row(item_list)}
                '''
        return html+css_html()
@frappe.whitelist()

def table_row(item_list):
    tablerow=''
    print(item_list)
    for i in item_list:
        print(i)
        tablerow+=f'''
                    { "".join([f"""
                    <tr>
                        <td><input type="checkbox">
                        </td>
                        <td>  <form action>
                        <input type="text" value={i}>
                        </form>
                        </td>
                        <td>  <form action>
                        <input type="text"  >
                        </form>
                        </form>
                        </td>
                        <td>  <form action>
                        <input type="text"  >
                        </form>
                        </form>
                        </td>
                        <td>  <form action>
                        <input type="text"  >
                        </form>
                        </form>
                        </td> <td>  <form action>
                        <input type="text"  >
                        </form>
                        </form>
                        </td>
                        <td>  <form action>
                        <input type="text"  >
                        </form>
                        </form>
                        </td>
                        <td>  <form action>
                        <input type="text"  >
                        </form>
                        </form>
                        </td>
                        <td>  <form action>
                        <input type="text"  >
                        </form>
                        </form>
                        </td>
                        <td>  <form action>
                        <input type="text"  >
                        </form>
                        </form>
                        </td>
                        <td>  <form action>
                        <input type="text"  >
                        </form>
                        </form>
                        </td>
                        <td>  <form action>
                        <input type="text"  >
                        </form>
                        </form>
                        </td>
                        <td>  <form action>
                        <input type="text"  >
                        </form>
                        </form>
                        </td>
                        <td>  <form action>
                        <input type="text"  >
                        </form>
                        </form>
                        </td>
                        <td>  <form action>
                        <input type="text"  >
                        </form>
                        </form>
                        </td>
                        <td id=last_cell>  <form action>
                        <input type="text"  >
                        </form>
                        </form>
                        </td>
                    </tr>
                 """])}
                '''
    return button()+tablerow+css_html()+'</table><br>'
def button():
    frappe.errprint("dfhjklbn")
    button=f''' 
        <button onclick="myCreateFunction()">Add row</button>
        <button onclick="myDeleteFunction()">Delete row</button>
    '''
    return button+script()
def css_html():
    css='''
    <style>
        table,tr,th,td{
            border: 1px solid black;
        }
    '''
    return css

def script():
    script='''
                
            <script>
            function myCreateFunction() {
                var table = document.getElementById("table");
                var lastvalue=document.getElementById("table");
                console.log(lastvalue)
                var row = table.insertRow(-1);
                var cell1 = row.insertCell(0);
                var cell2 = row.insertCell(1);
                cell1.innerHTML = "NEW CELL1";
                cell2.innerHTML = "NEW CELL2";
            }
            function myDeleteFunction() {
                document.getElementById("table").deleteRow(-1);
                }
            </script>
    
    '''
    return script
    