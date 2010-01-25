@echo off
START "" javaw -Duser.home=Data\. -cp Data\lib\freemind.jar;Data\lib\ant\lib\jaxb-api.jar;Data\lib\ant\lib\jaxb-impl.jar;Data\lib\ant\lib\jaxb-libs.jar;Data\lib\ant\lib\namespace.jar;Data\lib\ant\lib\relaxngDatatype.jar;Data\lib\ant\lib\xsdlib.jar;Data\lib\ant\lib\jax-qname.jar;Data\lib\ant\lib\sax.jar;Data\lib\ant\lib\dom.jar freemind.main.FreeMind %1%
