/*
 * File: app/view/ui/offeringsEditor.js
 * Date: Tue Jan 14 2014 10:49:25 GMT+0100 (CET)
 *
 * This file was generated by Ext Designer version 1.2.3.
 * http://www.sencha.com/products/designer/
 *
 * This file will be auto-generated each and everytime you export.
 *
 * Do NOT hand edit this file.
 */

Ext.define('istsos.view.ui.offeringsEditor', {
    extend: 'Ext.tab.Panel',

    minHeight: 400,
    title: '',
    activeTab: 0,

    initComponent: function() {
        var me = this;

        Ext.applyIf(me, {
            items: [
                {
                    xtype: 'panel',
                    height: 450,
                    minHeight: 400,
                    title: 'Offerings',
                    items: [
                        {
                            xtype: 'panel',
                            border: 0,
                            title: '',
                            items: [
                                {
                                    xtype: 'gridpanel',
                                    id: 'gridoff',
                                    margin: 8,
                                    maxHeight: 250,
                                    minHeight: 150,
                                    title: '',
                                    forceFit: true,
                                    store: 'gridofferings',
                                    viewConfig: {

                                    },
                                    dockedItems: [
                                        {
                                            xtype: 'toolbar',
                                            dock: 'top',
                                            items: [
                                                {
                                                    xtype: 'button',
                                                    id: 'btnNew',
                                                    text: 'New'
                                                },
                                                {
                                                    xtype: 'button',
                                                    disabled: true,
                                                    id: 'btnRemove',
                                                    text: 'Remove selected'
                                                }
                                            ]
                                        }
                                    ],
                                    columns: [
                                        {
                                            xtype: 'gridcolumn',
                                            dataIndex: 'name',
                                            text: 'Name'
                                        },
                                        {
                                            xtype: 'gridcolumn',
                                            dataIndex: 'description',
                                            text: 'Description'
                                        },
                                        {
                                            xtype: 'gridcolumn',
                                            dataIndex: 'procedures',
                                            text: 'Procedures'
                                        },
                                        {
                                            xtype: 'datecolumn',
                                            dataIndex: 'expiration',
                                            text: 'Expiration',
                                            format: 'c'
                                        },
                                        {
                                            xtype: 'booleancolumn',
                                            dataIndex: 'active',
                                            text: 'Active'
                                        }
                                    ]
                                },
                                {
                                    xtype: 'form',
                                    border: 0,
                                    hidden: true,
                                    id: 'frmOfferings',
                                    bodyPadding: 10,
                                    title: '',
                                    trackResetOnLoad: true,
                                    items: [
                                        {
                                            xtype: 'fieldset',
                                            title: 'Offerings',
                                            items: [
                                                {
                                                    xtype: 'textfield',
                                                    id: 'offName',
                                                    name: 'name',
                                                    fieldLabel: 'Name',
                                                    anchor: '100%'
                                                },
                                                {
                                                    xtype: 'textfield',
                                                    name: 'description',
                                                    fieldLabel: 'Description',
                                                    anchor: '100%'
                                                },
                                                {
                                                    xtype: 'datefield',
                                                    name: 'expiration',
                                                    fieldLabel: 'Expiration',
                                                    format: 'c',
                                                    anchor: '100%'
                                                },
                                                {
                                                    xtype: 'checkboxfield',
                                                    name: 'active',
                                                    fieldLabel: 'Visibility',
                                                    boxLabel: 'enabled',
                                                    anchor: '100%'
                                                }
                                            ]
                                        }
                                    ],
                                    dockedItems: [
                                        {
                                            xtype: 'toolbar',
                                            ui: 'footer',
                                            dock: 'bottom',
                                            layout: {
                                                pack: 'center',
                                                type: 'hbox'
                                            },
                                            items: [
                                                {
                                                    xtype: 'button',
                                                    id: 'btnForm',
                                                    text: 'Insert'
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                },
                {
                    xtype: 'panel',
                    height: 450,
                    layout: {
                        align: 'stretch',
                        type: 'vbox'
                    },
                    title: 'Offering-Procedure memberships',
                    items: [
                        {
                            xtype: 'panel',
                            border: 0,
                            height: 40,
                            html: 'Click & Drag procedures to add or remove membership',
                            padding: '16 16 8 16',
                            title: ''
                        },
                        {
                            xtype: 'panel',
                            autoRender: true,
                            border: 0,
                            minHeight: 400,
                            layout: {
                                align: 'stretch',
                                type: 'hbox'
                            },
                            flex: 1,
                            items: [
                                {
                                    xtype: 'panel',
                                    border: 0,
                                    height: 300,
                                    minHeight: 350,
                                    layout: {
                                        type: 'fit'
                                    },
                                    bodyPadding: 8,
                                    title: '',
                                    flex: 0.5,
                                    items: [
                                        {
                                            xtype: 'gridpanel',
                                            id: 'gridMembers',
                                            autoScroll: true,
                                            title: '',
                                            forceFit: true,
                                            store: 'proceduresMembers',
                                            viewConfig: {
                                                multiSelect: true,
                                                plugins: [
                                                    Ext.create('Ext.grid.plugin.DragDrop', {
                                                        ddGroup: 'offeringsprocedures',
                                                        dragGroup: 'gridMembers',
                                                        dropGroup: 'gridNonMembers'
                                                    })
                                                ]
                                            },
                                            dockedItems: [
                                                {
                                                    xtype: 'toolbar',
                                                    dock: 'top',
                                                    items: [
                                                        {
                                                            xtype: 'combobox',
                                                            id: 'cbOfferings',
                                                            fieldLabel: 'Choose an offering',
                                                            labelStyle: 'color: white;',
                                                            labelWidth: 140,
                                                            displayField: 'name',
                                                            store: 'cmbname',
                                                            valueField: 'name',
                                                            flex: 1
                                                        }
                                                    ]
                                                }
                                            ],
                                            columns: [
                                                {
                                                    xtype: 'gridcolumn',
                                                    dataIndex: 'name',
                                                    text: 'Name'
                                                },
                                                {
                                                    xtype: 'gridcolumn',
                                                    dataIndex: 'description',
                                                    text: 'Description'
                                                }
                                            ]
                                        }
                                    ]
                                },
                                {
                                    xtype: 'panel',
                                    border: 0,
                                    height: 300,
                                    minHeight: 350,
                                    layout: {
                                        type: 'fit'
                                    },
                                    bodyPadding: 8,
                                    title: '',
                                    flex: 0.5,
                                    items: [
                                        {
                                            xtype: 'gridpanel',
                                            id: 'gridNonMembers',
                                            title: 'Not members',
                                            forceFit: true,
                                            store: 'proceduresNonmembers',
                                            viewConfig: {
                                                multiSelect: true,
                                                plugins: [
                                                    Ext.create('Ext.grid.plugin.DragDrop', {
                                                        ddGroup: 'offeringsprocedures',
                                                        dragGroup: 'gridNonMembers',
                                                        dropGroup: 'gridMembers'
                                                    })
                                                ]
                                            },
                                            columns: [
                                                {
                                                    xtype: 'gridcolumn',
                                                    dataIndex: 'name',
                                                    text: 'Name'
                                                },
                                                {
                                                    xtype: 'gridcolumn',
                                                    dataIndex: 'description',
                                                    text: 'Description'
                                                }
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        });

        me.callParent(arguments);
    }
});