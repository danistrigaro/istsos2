/*
 * File: app/view/ui/config.js
 * Date: Tue Jan 28 2014 17:15:56 GMT+0100 (CET)
 *
 * This file was generated by Ext Designer version 1.2.3.
 * http://www.sencha.com/products/designer/
 *
 * This file will be auto-generated each and everytime you export.
 *
 * Do NOT hand edit this file.
 */

Ext.define('istsos.view.ui.config', {
    extend: 'Ext.form.Panel',

    border: 0,
    bodyPadding: 10,
    title: '',

    initComponent: function() {
        var me = this;

        Ext.applyIf(me, {
            items: [
                {
                    xtype: 'displayfield',
                    hidden: true,
                    id: 'messageField',
                    fieldStyle: 'color: red;',
                    name: 'message',
                    fieldLabel: 'Message',
                    labelStyle: 'color: red;',
                    anchor: '100%'
                },
                {
                    xtype: 'fieldset',
                    title: 'Proxy URL (optional)',
                    items: [
                        {
                            xtype: 'textfield',
                            fieldLabel: 'Url',
                            anchor: '100%'
                        },
                        {
                            xtype: 'textfield',
                            hidden: true,
                            fieldLabel: 'POST',
                            anchor: '100%'
                        }
                    ]
                },
                {
                    xtype: 'fieldset',
                    title: 'SensorML folder',
                    items: [
                        {
                            xtype: 'textfield',
                            name: 'smlpath',
                            fieldLabel: 'Path',
                            anchor: '100%'
                        }
                    ]
                },
                {
                    xtype: 'fieldset',
                    title: 'Virtual procedures',
                    items: [
                        {
                            xtype: 'textfield',
                            name: 'vppath',
                            fieldLabel: 'Path',
                            anchor: '100%'
                        }
                    ]
                },
                {
                    xtype: 'fieldset',
                    title: 'Coordinate system',
                    items: [
                        {
                            xtype: 'textfield',
                            name: 'defaultepsg',
                            fieldLabel: 'Default EPSG',
                            anchor: '100%'
                        },
                        {
                            xtype: 'textfield',
                            name: 'permittedepsg',
                            fieldLabel: 'Permitted EPSG',
                            anchor: '100%'
                        },
                        {
                            xtype: 'textfield',
                            name: 'xaxisname',
                            fieldLabel: 'X axis name',
                            anchor: '100%'
                        },
                        {
                            xtype: 'textfield',
                            name: 'yaxisname',
                            fieldLabel: 'Y axis name',
                            anchor: '100%'
                        },
                        {
                            xtype: 'textfield',
                            name: 'zaxisname',
                            fieldLabel: 'Z axis name',
                            anchor: '100%'
                        }
                    ]
                }
            ]
        });

        me.callParent(arguments);
    }
});