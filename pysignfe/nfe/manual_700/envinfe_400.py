# -*- coding: utf-8 -*-
import os

from pysignfe.xml_sped import *
from pysignfe.nfe.manual_500 import envinfe_310
from pysignfe.nfe.manual_700 import ESQUEMA_ATUAL
from .nfe_400 import NFe
from .consrecinfe_400 import ProtNFe

DIRNAME = os.path.dirname(__file__)

class EnviNFe(envinfe_310.EnviNFe):
    def __init__(self):
        super(EnviNFe, self).__init__()
        self.caminho_esquema = os.path.join(DIRNAME, u'schema/', ESQUEMA_ATUAL + u'/')
        self.arquivo_esquema = u'enviNFe_v4.00.xsd'
        self.versao  = TagDecimal(nome=u'enviNFe', codigo=u'AP02', propriedade=u'versao', namespace=NAMESPACE_NFE, valor=u'4.00', raiz=u'/')
        
    def get_xml(self):
        return super(EnviNFe, self).get_xml()

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.versao.xml = arquivo
            self.idLote.xml = arquivo
            self.indSinc.xml = arquivo
            self.NFe = self.le_grupo('//enviLote/NFe', NFe)

        return self.xml

    @property
    def xml(self):
        return self._xml

    @xml.setter
    def xml(self, arquivo):
        self.set_xml(arquivo)
        self._xml = arquivo
    

class InfRec(envinfe_310.InfRec):
    def __init__(self):
        super(InfRec, self).__init__()


class RetEnviNFe(envinfe_310.RetEnviNFe):
    def __init__(self):
        super(RetEnviNFe, self).__init__()
        self.infRec   = InfRec()
        ##Caso processamento sincrono do lote, dados do processamento sao recebidos na mesma conexao
        self.protNFe  = ProtNFe()
        self.caminho_esquema = os.path.join(DIRNAME, u'schema/', ESQUEMA_ATUAL + u'/')
        self.arquivo_esquema = u'retEnviNFe_v4.00.xsd'
        
    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        xml += self.versao.xml
        xml += self.tpAmb.xml
        xml += self.verAplic.xml
        xml += self.cStat.xml
        xml += self.xMotivo.xml
        xml += self.cUF.xml
        xml += self.dhRecbto.xml
        xml += self.infRec.xml
        xml += self.protNFe.xml
        xml += u'</retEnviNFe>'
        return xml
        
    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.versao.xml   = arquivo
            self.tpAmb.xml    = arquivo
            self.verAplic.xml = arquivo
            self.cStat.xml    = arquivo
            self.xMotivo.xml  = arquivo
            self.cUF.xml      = arquivo
            self.dhRecbto.xml = arquivo
            self.infRec.xml   = arquivo
            self.protNFe.xml  = arquivo
       
    @property
    def xml(self):
        return self._xml

    @xml.setter
    def xml(self, arquivo):
        self.set_xml(arquivo)
        self._xml = arquivo