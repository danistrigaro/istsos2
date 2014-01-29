/*
 * File: app/store/gridObservedProperties.js
 * Date: Tue Jan 28 2014 17:15:56 GMT+0100 (CET)
 *
 * This file was generated by Ext Designer version 1.2.3.
 * http://www.sencha.com/products/designer/
 *
 * This file will be auto-generated each and everytime you export.
 *
 * Do NOT hand edit this file.
 */

Ext.define('istsos.store.gridObservedProperties', {
    extend: 'Ext.data.Store',

    constructor: function(cfg) {
        var me = this;
        cfg = cfg || {};
        me.callParent([Ext.apply({
            storeId: 'gridobservedproperties',
            proxy: {
                type: 'ajax',
                url: '',
                reader: {
                    type: 'json',
                    idProperty: 'definition',
                    messageProperty: 'message',
                    root: 'data'
                }
            },
            fields: [
                {
                    name: 'name',
                    type: 'string'
                },
                {
                    name: 'definition',
                    type: 'string'
                },
                {
                    name: 'description',
                    type: 'string'
                },
                {
                    name: 'procedures',
                    type: 'string'
                },
                {
                    name: 'constraint'
                }
            ]
        }, cfg)]);
    }
});