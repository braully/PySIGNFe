# -*- coding: utf-8 -*-

import os

from pysignfe.xml_sped import *

DIRNAME = os.path.dirname(__file__)

class NFeCabecMsg(XMLNFe):
    def __init__(self):
        super(NFeCabecMsg, self).__init__()
        self.webservice = u''
        self.cUF         = TagInteiro(nome=u'cUF'        , codigo=u'', raiz=u'//cabecMsg', tamanho=[2, 2], valor=35)
        self.versaoDados = TagDecimal(nome=u'versaoDados', codigo=u'', raiz=u'//cabecMsg', tamanho=[1, 4], valor=u'4.00')

    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        xml += u'<nfeCabecMsg xmlns="http://www.portalfiscal.inf.br/nfe/wsdl/' + self.webservice + u'">'
        xml += self.cUF.xml
        xml += self.versaoDados.xml
        xml += u'</nfeCabecMsg>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.cUF.xml         = arquivo
            self.versaoDados.xml = arquivo

        return self.xml

    @property
    def xml(self):
        return self.get_xml()

    @xml.setter
    def xml(self, arquivo):
        self.set_xml(arquivo)


class NFeDadosMsg(XMLNFe):
    def __init__(self):
        super(NFeDadosMsg, self).__init__()
        self.webservice = u''
        self.dados = None
        self.versaoDados = TagDecimal(nome=u'versaoDados', codigo=u'', raiz=u'//cabecMsg', tamanho=[1, 4], valor=u'4.00')

    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        xml += u'<nfeDadosMsg xmlns="http://www.portalfiscal.inf.br/nfe/wsdl/' + self.webservice + u'">'
        xml += tira_abertura(self.dados.xml)
        xml += u'</nfeDadosMsg>'
        return xml

    def set_xml(self, arquivo):
        pass

    @property
    def xml(self):
        return self.get_xml()

    @xml.setter
    def xml(self, arquivo):
        self.set_xml(arquivo)




class SOAPEnvio(XMLNFe):
    def __init__(self):
        super(SOAPEnvio, self).__init__()
        self.webservice = u''
        self.metodo = u''
        self.cUF    = None
        self.envio  = None
        #self.nfeCabecMsg = NFeCabecMsg()
        self.nfeDadosMsg = NFeDadosMsg()
        self._header = {u'content-type': u'application/soap+xml; charset=utf-8'}

    def get_xml(self):
        self.nfeDadosMsg.webservice = self.webservice
        self.nfeDadosMsg.dados = self.envio

        self._header[u'content-type'] = u'application/soap+xml; charset=utf-8; action="http://www.portalfiscal.inf.br/nfe/wsdl/' + self.webservice + u'"'

        xml = XMLNFe.get_xml(self)
        xml += ABERTURA
        xml += u'<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope">'
        xml +=     u'<soap:Body>'
        xml +=             self.nfeDadosMsg.xml
        xml +=     u'</soap:Body>'
        xml += u'</soap:Envelope>'
        return xml

    def set_xml(self):
        pass

    @property
    def xml(self):
        return self.get_xml()

    @xml.setter
    def xml(self, arquivo):
        self.set_xml(arquivo)


    def get_header(self):
        header = self._header
        return header

    header = property(get_header)


class SOAPRetorno(XMLNFe):
    def __init__(self):
        super(SOAPRetorno, self).__init__()
        self.webservice = u''
        self.metodo = u''
        self.resposta = None

    def get_xml(self):
        xml = XMLNFe.get_xml(self)
        xml += ABERTURA
        xml += u'<soap:Envelope xmlns:soap="http://www.w3.org/2003/05/soap-envelope">'
        xml +=     u'<soap:Body>'
        xml +=         u'<' + self.metodo + u'Result xmlns="http://www.portalfiscal.inf.br/nfe/wsdl/' + self.webservice + u'">'
        xml +=             self.resposta.xml
        xml +=         u'</' + self.metodo + u'Result>'
        xml +=     u'</soap:Body>'
        xml += u'</soap:Envelope>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.resposta.xml = arquivo

    @property
    def xml(self):
        return self.get_xml()

    @xml.setter
    def xml(self, arquivo):
        self.set_xml(arquivo)

