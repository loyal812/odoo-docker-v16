/** @odoo-module **/

import { registry } from "@web/core/registry";
import { Many2ManyTagsField } from "@web/views/fields/many2many_tags/many2many_tags_field";
import { useService } from "@web/core/utils/hooks";

class Many2ManyTagsExtensionDDT extends Many2ManyTagsField {
  setup() {
    //eredito il setup dalla classe padre
    super.setup();
    //chiamo i servizi
    this.orm = useService("orm");
    this.action = useService("action");
    this.dialog = useService("dialog");
    let ddt_date_invoice = this.props.record.data.ddt_date_invoice;
    if (ddt_date_invoice) {
      let ddt_array = ddt_date_invoice.split(",");
      let i = 0;
      for (let x of this.props.record.data.delivery_note_ids.records) {
        x.data.display_name = ddt_array[i];
        i++;
      }
    }
    console.log(this);
  }
  openAction(record) {
    let action = {
      type: "ir.actions.act_window",
      res_model: record.resModel,
      res_id: record.resId,
      views: [[false, "form"]],
      target: "self",
    };
    return this.action.doAction(action);
  }
  getTagProps(record) {
    let records = super.getTagProps(record);
    records.onClick = (e) => {
      e.preventDefault();
      e.stopPropagation();
      this.openAction(record);
    };
    return records;
  }
}

class Many2ManyTagsExtensionInvoice extends Many2ManyTagsField {
  setup() {
    //eredito il setup dalla classe padre
    super.setup();
    //chiamo i servizi
    this.orm = useService("orm");
    this.action = useService("action");
    this.dialog = useService("dialog");
  }
  openAction(record) {
    let action = {
      type: "ir.actions.act_window",
      res_model: record.resModel,
      res_id: record.resId,
      views: [[false, "form"]],
      target: "self",
    };
    return this.action.doAction(action);
  }
  getTagProps(record) {
    let records = super.getTagProps(record);
    records.onClick = (e) => {
      e.preventDefault();
      e.stopPropagation();
      this.openAction(record);
    };
    return records;
  }
}

registry
  .category("fields")
  .add("many2many_tags_ddt", Many2ManyTagsExtensionDDT);
registry
  .category("fields")
  .add("many2many_tags_invoice", Many2ManyTagsExtensionInvoice);

/*
class Many2ManyTagsExtensionDDTDate extends Many2ManyTagsField {
     setup() {
        //eredito il setup dalla classe padre
        super.setup();
        //chiamo i servizi
        this.orm = useService("orm");
        this.action = useService("action");
        this.dialog = useService("dialog");
        this.ddt_invoices = this.props.record.data.ddt_invoices_ids.records;
        for (let record of this.ddt_invoices){
            let res = this.orm.call('stock.delivery.note','read',[record.resId],{});
            let result = res.then((response) => {console.log(response); return response;})
            
            //console.log(result);
        }
        console.log(this); 
    }
    openAction(record) {
        let action = {
            type: "ir.actions.act_window",
            res_model: record.resModel,
            res_id:  record.resId,
            views: [[false, "form"]],
            target: "self"

        }
        return this.action.doAction(action);
    }
    getTagProps(record) {
        let records = super.getTagProps(record);
        records.onClick = (e) => {
            e.preventDefault();
            e.stopPropagation();
            this.openAction(record);  
        }
        return records;
    }
}


*/
