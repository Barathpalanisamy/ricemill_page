frappe.pages["manufacturing-rice"].on_page_load = function (wrapper) {
  var page = frappe.ui.make_app_page({
    parent: wrapper,
    title: "Rice Mill Manufacturing",
    single_column: true,
  });
  new erpnext.Ricemill(page);
};
var me;
erpnext.Ricemill = class Ricemill {
  constructor(page) {
    this.page = page;
    me = this;
    this.make_form();
  }
  make_form() {
    this.form = new frappe.ui.FieldGroup({
      fields: [
        {
          label: "Item To Manufacture",
          fieldtype: "Link",
          fieldname: "item_to_manufacture",
          options: "Item",
          change: () =>
            frappe.call({
              method: "retail.retail.page.manufacturing_rice.ricemill.setup",
              args: {
                ricemill: this.form.get_value("item_to_manufacture"),
              },
              callback: function (r) {
                this.form.get_field("html1").html(r.message);
              }.bind(this),
            }),
        },
        {
          fieldtype: "Column Break",
        },
        {
          label: "Bom No",
          fieldname: "bom_no",
          fieldtype: "Link",
          options: "BOM",
        },

        {
          fieldtype: "Section Break",
        },
        {
          fieldname: "html1",
          fieldtype: "HTML",
        },
        {
          fieldname: "html2",
          fieldtype: "HTML",
        },
      ],

      body: this.page.body,
    });
    this.form.make();
  }
};

function myFunction(ricemill) {
  var a = document.getElementById("qty").value;
  var b = document.getElementById("bom_name").value;
  if (a && b) {
    frappe.call({
      method:
        "retail.retail.page.manufacturing_rice.work_order.work_order_creation",
      args: { a: a, b: b, c: ricemill },
    });
    frappe.call({
      method: "retail.retail.page.manufacturing_rice.ricemill.function",
      args: { ricemill: ricemill },
      callback(r) {
        me.form.get_field("html1").html(r.message);
		document.getElementById("initialize").style.display = 'none'
		
		
      },
    });
  }
}


class Stopwatch {
			constructor(display, results) {
				me.running = false;
				me.display = display;
				me.results = results;
				me.laps = [];
				me.reset();
				me.print(me.times);
			}
			
			reset() {
				me.times = [ 0, 0, 0 ];
			}
			
			start() {
				if (!me.time) me.time = performance.now();
				if (!me.running) {
					me.running = me;
					requestAnimationFrame(me.step.bind(me));
				}
			}
			
			lap() {
				let times = me.times;
				let li = document.createElement('li');
				li.innerText = me.format(times);
				me.results.appendChild(li);
			}
			
			stop() {
				me.running = false;
				me.time = null;
			}

			restart() {
				if (!me.time) me.time = performance.now();
				if (!me.running) {
					me.running = true;
					requestAnimationFrame(me.step.bind(me));
				}
				me.reset();
			}
			
			clear() {
				clearChildren(me.results);
			}
			
			step(timestamp) {
				if (!me.running) return;
				me.calculate(timestamp);
				me.time = timestamp;
				me.print();
				requestAnimationFrame(me.step.bind(me));
			}
			
			calculate(timestamp) {
				var diff = timestamp - me.time;
				// Hundredths of a second are 100 ms
				me.times[2] += diff / 10;
				// Seconds are 100 hundredths of a second
				if (me.times[2] >= 100) {
					me.times[1] += 1;
					me.times[2] -= 100;
				}
				// Minutes are 60 seconds
				if (me.times[1] >= 60) {
					me.times[0] += 1;
					me.times[1] -= 60;
				}
			}
			
			print() {
				me.display.innerText = me.format(this.times);
			}
			
			format(times) {
				return `\
		${pad0(times[0], 2)}:\
		${pad0(times[1], 2)}:\
		${pad0(Math.floor(times[2]), 2)}`;
			}
		}

		function pad0(value, count) {
			var result = value.toString();
			for (; result.length < count; --count)
				result = '0' + result;
			return result;
		}

		function clearChildren(node) {
			while (node.lastChild)
				node.removeChild(node.lastChild);
		}

		let stopwatch = new Stopwatch(
			document.querySelector('.stopwatch'),
			document.querySelector('.results'));

