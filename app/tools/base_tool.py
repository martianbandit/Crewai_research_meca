from typing import Any, Dict, Optional, List
from abc import ABC, abstractmethod
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
import logging
from datetime import datetime

class ToolResult(BaseModel):
    """Modèle standardisé pour les résultats des outils"""
    success: bool = Field(default=True, description="Indique si l'opération a réussi")
    data: Any = Field(description="Données résultantes de l'opération")
    error: Optional[str] = Field(default=None, description="Message d'erreur si échec")
    timestamp: datetime = Field(default_factory=datetime.now, description="Horodatage de l'opération")
    metadata: Dict = Field(default_factory=dict, description="Métadonnées additionnelles")

class MechanicBaseTool(BaseTool, ABC):
    """Outil de base pour les mécaniciens avec fonctionnalités étendues"""
    
    name: str = ""
    description: str = ""
    version: str = "1.0.0"
    category: str = Field(default="general", description="Catégorie de l'outil")
    requires_api_key: bool = Field(default=False, description="Indique si l'outil nécessite une clé API")
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.logger = logging.getLogger(self.__class__.__name__)
        self._setup_logging()
    
    def _setup_logging(self):
        """Configure le logging pour l'outil"""
        if not self.logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(logging.INFO)
    
    def _handle_error(self, error: Exception, context: Dict = None) -> ToolResult:
        """
        Gestion standardisée des erreurs
        
        Args:
            error: L'exception survenue
            context: Contexte additionnel de l'erreur
            
        Returns:
            ToolResult: Résultat formaté avec l'erreur
        """
        error_message = f"{self.name} error: {str(error)}"
        self.logger.error(error_message, exc_info=True, extra=context or {})
        
        return ToolResult(
            success=False,
            data=None,
            error=error_message,
            metadata=context or {}
        )
    
    def _format_result(self, data: Any, metadata: Dict = None) -> ToolResult:
        """
        Formate le résultat de l'outil
        
        Args:
            data: Données à formater
            metadata: Métadonnées additionnelles
            
        Returns:
            ToolResult: Résultat formaté
        """
        return ToolResult(
            data=data,
            metadata=metadata or {}
        )
    
    @abstractmethod
    def _run(self, *args: Any, **kwargs: Any) -> ToolResult:
        """
        Méthode abstraite à implémenter par les outils concrets
        
        Returns:
            ToolResult: Résultat de l'opération
        """
        raise NotImplementedError
    
    def run(self, *args: Any, **kwargs: Any) -> ToolResult:
        """
        Exécute l'outil avec gestion des erreurs et logging
        
        Returns:
            ToolResult: Résultat de l'opération
        """
        try:
            self.logger.info(f"Running {self.name}")
            result = self._run(*args, **kwargs)
            self.logger.info(f"{self.name} completed successfully")
            return result
        except Exception as e:
            return self._handle_error(e, {"args": args, "kwargs": kwargs})
    
    @property
    def tool_info(self) -> Dict:
        """
        Retourne les informations sur l'outil
        
        Returns:
            Dict: Informations sur l'outil
        """
        return {
            "name": self.name,
            "description": self.description,
            "version": self.version,
            "category": self.category,
            "requires_api_key": self.requires_api_key
        }
