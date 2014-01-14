/*
 * File: app/store/Constraint.js
 * Date: Tue Jan 14 2014 10:49:25 GMT+0100 (CET)
 *
 * This file was generated by Ext Designer version 1.2.3.
 * http://www.sencha.com/products/designer/
 *
 * This file will be auto-generated each and everytime you export.
 *
 * Do NOT hand edit this file.
 */

Ext.define('istsos.store.Constraint', {
    extend: 'Ext.data.Store',

    constructor: function(cfg) {
        var me = this;
        cfg = cfg || {};
        me.callParent([Ext.apply({
            storeId: 'constraint',
            data: [
                {
                    name: ' -- ',
                    'value': 0
                },
                {
                    'name': 'Greater then',
                    'value': 1
                },
                {
                    'name': 'Less then',
                    'value': 2
                },
                {
                    'name': 'Between',
                    'value': 3
                },
                {
                    'name': 'Value list',
                    'value': 4
                },
                
            ],
            proxy: {
                type: 'ajax',
                reader: {
                    type: 'json',
                    root: 'data'
                }
            },
            fields: [
                {
                    name: 'name'
                },
                {
                    name: 'value'
                }
            ]
        }, cfg)]);
    }
});