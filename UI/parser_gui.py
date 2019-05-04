from PyQt5 import uic, QtWidgets, QtCore, QtGui
import sys
import os
import pickle
import gzip
from core import stix_telemetry_parser 
from core import stix_global
from core import stix_writer
from core import stix_writer_sqlite
from core import odb
import os
from UI import mainwindow_rc5
from UI.mainwindow import Ui_MainWindow

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from PyQt5.QtCore import QThread, pyqtSignal
import re
import binascii
import xmltodict
from io import BytesIO

class StixDataReader(QThread):
    """
    thread
    """
    dataLoaded= pyqtSignal(list)
    error= pyqtSignal(str)
    info= pyqtSignal(str)
    def __init__(self,filename):
        super(StixDataReader,self).__init__()
        self.filename=filename
        self.data=[]

    def run(self):
        self.data=[]
        filename=self.filename
        if filename.endswith('.pklz'):
            self.info.emit(('Decompressing {}').format(filename))
            f=gzip.open(filename,'rb')
            self.info.emit(('Loading ...'))
            self.data=pickle.load(f)['packet']
            f.close()
        elif filename.endswith('.pkl'):
            f=open(filename,'rb')
            self.info.emit('Loading ...')
            self.data=pickle.load(f)['packet']
            f.close()
        elif filename.endswith('.dat'):
            self.parseRawFile()
        elif filename.endswith(('.db','.sqlite')):
            self.read_packet_from_db(filename)
        elif filename.endswith('.xml'):
            self.parseESOCXmlFile(filename)
        self.dataLoaded.emit(self.data)
    def read_packet_from_db(self,filename):
        self.info.emit(('Loading data from {}').format(filename))
        db=odb.ODB(filename)

        self.data=db.get_packets()


    def parseESOCXmlFile(self,in_filename):
        packets=[]
        try:
            fd=open(in_filename)
        except Exception as e:
            self.error.emit('Failed to open {}'.format(str(e)))
        else:

            self.info.emit(('Parsing {}').format(in_filename))
            doc = xmltodict.parse(fd.read())
            for e in doc['ns2:ResponsePart']['Response']['PktRawResponse']['PktRawResponseElement']:
                packet={'id':e['@packetID'], 'raw':e['Packet']}
                packets.append(packet)
        num=len(packets)
        freq=1
        if num > 100:
            freq=num/100

        for i,packet in enumerate(packets):
            data_hex=packet['raw']
            data_binary= binascii.unhexlify(data_hex)
            in_file=BytesIO(data_binary[76:])
            status, header, parameters, param_type, param_desc, num_bytes_read = stix_telemetry_parser.parse_one_packet(
                in_file, self)
            if i%freq==0:
                self.info.emit("{.0f}% loaded".format(100*i/num))
            self.data.append({'header':header,'parameter':parameters})

    def parseRawFile(self):
        filename=self.filename

        try:
            in_file=open(filename, 'rb') 
        except Exception as e:
            self.error.emit('Failed to open {}'.format(str(e)))
        else:
            size=os.stat(filename).st_size
            percent=int(size/100)
            num_packets = 0
            total_read= 0
            stix_writer=None
            #st_writer.register_run(in_filename)
            total_packets=0
            self.data=[]
            selected_spid=0
            last_percent=0
            while True:
                status, header, parameters, param_type, param_desc, num_bytes_read = stix_telemetry_parser.parse_one_packet(in_file, 
                        None,selected_spid, output_param_type='tree')
                total_read+=num_bytes_read
                total_packets += 1
                if status == stix_global.NEXT_PACKET:
                    continue
                if status == stix_global.EOF:
                    break

                if int(total_read/percent) > int(last_percent):
                    self.info.emit("{:.0f}% loaded".format(100*total_read/size))
                last_percent= total_read/percent

                
                self.data.append({'header':header,'parameter':parameters})





class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('UI/mainwindow.ui', self)


        self.initialize()


    def initialize(self):
        self.tabWidget.setCurrentIndex(0)
        self.actionExit.triggered.connect(self.close)
        self.action_Plot.setEnabled(False)

        self.actionNext.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_ArrowForward))
        self.actionPrevious.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_ArrowBack))
        self.action_Open.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_DialogOpenButton))
        self.actionSave.setIcon(self.style().standardIcon(QtWidgets.QStyle.SP_DriveFDIcon))

        self.actionSave.triggered.connect(self.save)


        self.action_Open.triggered.connect(self.getOpenFilename)


        self.paramTreeWidget_header=QtWidgets.QTreeWidgetItem(['Name','description','raw','Eng value'])
        self.paramTreeWidget.setHeaderItem(self.paramTreeWidget_header)

        self.packetTreeWidget_header=QtWidgets.QTreeWidgetItem(['Timestamp','Description'])
        self.packetTreeWidget.setHeaderItem(self.packetTreeWidget_header)



        self.actionNext.triggered.connect(self.nextPacket)
        self.actionPrevious.triggered.connect(self.previousPacket)
        self.actionAbout.triggered.connect(self.about)
        
        self.actionPrevious.setEnabled(False)
        self.actionNext.setEnabled(False)
        self.actionSave.setEnabled(False)
        self.action_Plot.setEnabled(False)
        self.actionLog.triggered.connect(self.dockWidget_2.show)
        self.actionSet_IDB.triggered.connect(self.onSetIDBClicked)

        self.plotButton.clicked.connect(self.onPlotButtonClicked)
        self.action_Plot.triggered.connect(self.onPlotActionClicked)

        self.current_row=0

        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)
        self.gridLayout.addWidget(self.canvas, 1, 0, 1, 14)
        self.savePlotButton.clicked.connect(self.savePlot)
        self.actionPaste.triggered.connect(self.paste)
        
    def savePlot(self):
        if self.figure.get_axes():
            filename= str(QtWidgets.QFileDialog.getSaveFileName(self, "Save file", "", "*.pdf *.png *.svg *.jpg")[0])
            if filename:
                self.figure.savefig(filename)
                self.showMessage(('Saved to %s.'%filename),0)
        

        else:
            msgBox = QtWidgets.QMessageBox()
            msgBox.setIcon(QtWidgets.QMessageBox.Information)
            msgBox.setText('The canvas is empty!')
            msgBox.setWindowTitle("STIX DATA VIEWER")
            msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
            msgBox.exec_()



    def paste(self):
        raw_hex= QtWidgets.QApplication.clipboard().text()
        if not raw_hex:
            self.showMessage('No data in the clipboard.',0)
            return 
        data_hex= re.sub(r"\s+", "", raw_hex)
        try:
            data_binary = binascii.unhexlify(data_hex)
            in_file=StringIO(data_binary)
            status, header, parameters, param_type, param_desc, num_bytes_read = stix_telemetry_parser.parse_one_packet(
                in_file, self)
            data=[{'header':header,'parameter':parameters}]
            self.showMessage(('%d bytes read from the clipboard'%num_bytes_read),1)
            self.onDataLoaded(data)
        except TypeError:
            self.showMessage('Failed to parse the packet',0)


    def showMessage(self,msg, destination=0):
        if destination != 1:
            self.statusbar.showMessage(msg)
        if destination !=0 :
            self.listWidget_2.addItem(msg)

    def onSetIDBClicked(self):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Information)
        path = os.path.dirname(os.path.realpath(__file__))
        msgBox.setText("Please copy file idb.sqlite to the folder %s/idb/ to change IDB !"%path)
        msgBox.setWindowTitle("STIX DATA VIEWER")
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgBox.exec_()


    def save(self):
        self.output_filename = str(QtWidgets.QFileDialog.getSaveFileName(self, "Save file", "", ".pklz .pkl .db .sqlite")[0])
        
        if not self.output_filename.endswith(('.pklz','.pkl','.db','.sqlite')):
            msg=('unsupported file format !')
            return
        msg=('Writing data to file %s')%self.output_filename
        self.showMessage(msg,2)

        if self.output_filename.endswith(('.pklz','.pkl')):
            stw=stix_writer.stix_writer(self.output_filename)
            stw.register_run(str(self.input_filename))
            stw.write_all(self.data)
            stw.done()
        elif self.output_filename.endswith('.db'):
            stw=stix_writer_sqlite.stix_writer(self.output_filename)
            stw.register_run(str(self.input_filename))
            stw.write_all(self.data)
            stw.done()

        self.showMessage((('Data has been written to %s ')%self.output_filename),2)
        
    def setListViewSelected(self,row):
        #index = self.model.createIndex(row, 0);
        #if index.isValid():
        #    self.model.selectionModel().select( index, QtGui.QItemSelectionModel.Select) 
        pass

    def about(self):
        msgBox = QtWidgets.QMessageBox()
        msgBox.setIcon(QtWidgets.QMessageBox.Information)
        msgBox.setText("STIX raw data parser and viewer, hualin.xiao@fhnw.ch")
        msgBox.setWindowTitle("Stix data viewer")
        msgBox.setStandardButtons(QtWidgets.QMessageBox.Ok)
        msgBox.exec_()


    def nextPacket(self):
        self.current_row+=1
        self.showPacket(self.current_row)
        self.setListViewSelected(self.current_row)
    def previousPacket(self):
        self.current_row-=1
        self.showPacket(self.current_row)
        self.setListViewSelected(self.current_row)

    def getOpenFilename(self):
        self.input_filename = QtWidgets.QFileDialog.getOpenFileName(None,'Select file', '.', 
                'STIX data file (*.dat *.pkl *.pklz *xml *.db)')[0]
        if not self.input_filename:
            return
        self.openFile(self.input_filename)

    def openFile(self,filename):
        msg='Loading file %s ...'%filename
        self.showMessage(msg, 2)

        self.dataReader=StixDataReader(filename)
        self.dataReader.dataLoaded.connect(self.onDataLoaded)
        self.dataReader.error.connect(self.onDataReaderError)
        self.dataReader.info.connect(self.onDataReaderInfo)
        self.dataReader.start()

    def onDataReaderInfo(self,msg):
        self.showMessage(msg,0)

    def onDataReaderError(self,msg):
        self.showMessage(msg,2)


    def onDataLoaded(self,data):
        self.data=data
        total_packets=len(self.data)

        self.packetTreeWidget.clear()
        self.displayPackets()
        if self.data:
            self.actionPrevious.setEnabled(True)
            self.actionNext.setEnabled(True)
            self.actionSave.setEnabled(True)
            self.action_Plot.setEnabled(True)







    def displayPackets(self):
        for p in self.data:
            header=p['header']
            root=QtWidgets.QTreeWidgetItem(self.packetTreeWidget)
            root.setText(0,'{:.2f}'.format(header['time']))
            root.setText(1,('TM({},{}) - {}').format(header['service_type'],header['service_subtype'],header['DESCR']))
        self.total_packets=len(self.data)
        self.showMessage((('%d packets loaded')%(self.total_packets)), 1)
        self.packetTreeWidget.currentItemChanged.connect(self.onPacketSelected)
        self.showPacket(0)
    
    def onPacketSelected(self, cur, pre):
        self.current_row=self.packetTreeWidget.currentIndex().row()
        self.showMessage((('Packet #%d selected') % self.current_row),0)
        self.showPacket(self.current_row)

    def showPacket(self,row):
        if not self.data:
            return
        header=self.data[row]['header']
        self.showMessage((('Packet %d / %d  %s ' )% (row, self.total_packets, header['DESCR'])),0)
        self.paramTreeWidget.clear()
        header_root=QtWidgets.QTreeWidgetItem(self.paramTreeWidget)
        header_root.setText(0,"Header")
        rows=len(header)
        for key, val in header.items():
            root=QtWidgets.QTreeWidgetItem(header_root)
            root.setText(0,key)
            root.setText(1,str(val))

        params=self.data[row]['parameter']
        param_root=QtWidgets.QTreeWidgetItem(self.paramTreeWidget)
        param_root.setText(0,"Parameters")
        self.showParameterTree(params,param_root)
        self.paramTreeWidget.expandItem(param_root)
        self.paramTreeWidget.expandItem(header_root)

    def showParameterTree(self, params, parent):
        for p in  params:
            root=QtWidgets.QTreeWidgetItem(parent)
            if not p:
                continue
            try:
                root.setText(0,p['name'])
                root.setText(1,p['descr'])
                root.setText(2,str(p['raw']))
                root.setText(3,str(p['value']))
                if 'child' in p:
                    if p['child']:
                        self.showParameterTree(p['child'],root)
            except KeyError:
                self.showMessage(('[Error  ]: keyError occurred when adding parameter'),1)
        self.paramTreeWidget.itemDoubleClicked.connect(self.onTreeItemClicked)

    def walk(self,name, params, header, ret_x, ret_y,xaxis=0,data_type=0):
        if not params:
            return
        timestamp=header['time']
        for p in  params:
            if not p or 'raw' not in p:
                continue
            if name == p['name']:
                values=None
                if data_type==0:
                    values=p['raw']
                else:
                    values=p['value']
                try:
                    eng_value=None
                    if values is float or int:
                        eng_value=values
                    else:
                        eng_value=values[0]

                    if type(eng_value) is float or int:
                        ret_y.append(eng_value)
                        if xaxis==1:
                            ret_x.append(timestamp)
                    else:
                        self.showMessage((('Can not plot %s  ')%str(eng_value)),1)
                except IndexError:
                    self.showMessage((('%s has empty values')%str(p)),1)

            if 'child' in p:
                if p['child']:
                    self.walk(name, p['child'], header, ret_x, ret_y, xaxis,data_type)



    def onPlotButtonClicked(self):
        if not self.data:
            return 
        name=self.paramNameEdit.text()
        packet_selection=self.comboBox.currentIndex()
        xaxis_type=self.xaxisComboBox.currentIndex()
        data_type=self.dataTypeComboBox.currentIndex()

        timestamp=[]
        y=[]
        if packet_selection==0:
            packet_id=self.current_row
            params=self.data[packet_id]['parameter']
            header=self.data[packet_id]['header']
            self.walk(name, params,header,timestamp,y, xaxis_type,data_type)
        elif packet_selection==1:
            for packet in self.data:
                params=packet['parameter']
                header=packet['header']
                self.walk(name, params,header,timestamp,y,xaxis_type,data_type)

        ax=self.figure.add_subplot(111)
        ax.clear()
        if not y:
            self.showMessage('No data points',0)
        elif y:
            style=self.styleEdit.text()
            if not style:
                style='o-'
            title='%s'%str(name)
            desc=self.descLabel.text()
            if desc:
                title += '- %s'%desc

            ylabel='Raw value'
            if data_type==1:
                ylabel='Engineering  value'


            if xaxis_type ==0:
                ax.plot(y,style)
                ax.set_xlabel("Packet #")

            elif xaxis_type==1:
                x=[t-timestamp[0] for t in timestamp]
                ax.plot(x,y,style)
                ax.set_xlabel("Time - T0 (s)")
            else:
                #histogram
                nbins=len(set(y))
                ax.hist(y,nbins, density=True, facecolor='g', alpha=0.75)
                ax.set_xlabel("%s"%title)
                ylabel='Counts'

            ax.set_title(title)
            ax.set_ylabel(ylabel)

            self.canvas.draw()
            self.showMessage('The canvas updated!',0)

    def plotParameter(self,name=None, desc=None):
        self.tabWidget.setCurrentIndex(1)
        if name:
            self.paramNameEdit.setText(name)
        if desc:
            self.descLabel.setText(desc)

    def onPlotActionClicked(self):
        self.tabWidget.setCurrentIndex(1)
        self.plotParameter()


    def onTreeItemClicked(self, it, col):
        #print(it, col, it.text(0))
        self.plotParameter(it.text(0),it.text(1))



    def error(self,  msg, description=''):
        self.showMessage((('Error: %s - %s')% (msg,description)),1)

    def warning(self, msg, description=''):
        self.showMessage((('Warning: %s - %s')% (msg,description)),1)

    def info(self,  msg, description=''):
        self.showMessage((('Info: %s - %s')% (msg,description)),1)


if __name__ == '__main__':
    filename=None
    if len(sys.argv)>=2:
        filename=sys.argv[1]

    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    window.show()
    if filename:
        window.openFile(filename)
    sys.exit(app.exec_())
