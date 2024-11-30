import asyncio
from typing import Any, Callable, Coroutine, Dict, List
from functools import wraps
import streamlit as st
from concurrent.futures import ThreadPoolExecutor

class AsyncManager:
    """Gestionnaire de tâches asynchrones pour l'application"""
    
    _instance = None
    _executor = ThreadPoolExecutor(max_workers=4)
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AsyncManager, cls).__new__(cls)
        return cls._instance
    
    @staticmethod
    def run_async(func: Callable) -> Callable:
        """Décorateur pour exécuter une fonction de manière asynchrone"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            future = AsyncManager._executor.submit(func, *args, **kwargs)
            return future.result()
        return wrapper
    
    @staticmethod
    async def load_components():
        """Charge les composants de manière asynchrone"""
        if 'components_loaded' not in st.session_state:
            with st.spinner("Chargement des composants..."):
                # Chargement asynchrone des gestionnaires
                tasks = [
                    asyncio.create_task(AsyncManager._load_vector_store()),
                    asyncio.create_task(AsyncManager._load_tools()),
                    asyncio.create_task(AsyncManager._load_agents())
                ]
                await asyncio.gather(*tasks)
                st.session_state.components_loaded = True
    
    @staticmethod
    async def _load_vector_store():
        """Charge la base de données vectorielle"""
        from app.utils.vector_store_manager import VectorStoreManager
        if 'vector_store' not in st.session_state:
            st.session_state.vector_store = VectorStoreManager()
            # Chargement initial des bases
            await asyncio.gather(
                st.session_state.vector_store.load_vector_store("diagnostic_kb"),
                st.session_state.vector_store.load_vector_store("inspection_kb"),
                st.session_state.vector_store.load_vector_store("maintenance_kb")
            )
    
    @staticmethod
    async def _load_tools():
        """Charge les outils de manière asynchrone"""
        if 'tools' not in st.session_state:
            from app.tools.base_tool import BaseTool
            # Import dynamique des outils
            tools_module = __import__('app.tools', fromlist=['*'])
            st.session_state.tools = []
            for attr in dir(tools_module):
                if attr.endswith('Tool') and attr != 'BaseTool':
                    tool_class = getattr(tools_module, attr)
                    if issubclass(tool_class, BaseTool):
                        st.session_state.tools.append(tool_class())
    
    @staticmethod
    async def _load_agents():
        """Charge les agents de manière asynchrone"""
        if 'agents' not in st.session_state:
            from app.agents.specialized_agents import SpecializedAgents
            st.session_state.agents = SpecializedAgents()
    
    @staticmethod
    def cache_result(ttl_seconds: int = 3600):
        """Décorateur pour mettre en cache les résultats des fonctions"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                cache_key = f"{func.__name__}_{str(args)}_{str(kwargs)}"
                if cache_key not in st.session_state:
                    st.session_state[cache_key] = {
                        'result': func(*args, **kwargs),
                        'timestamp': asyncio.get_event_loop().time()
                    }
                elif (asyncio.get_event_loop().time() - 
                      st.session_state[cache_key]['timestamp']) > ttl_seconds:
                    st.session_state[cache_key] = {
                        'result': func(*args, **kwargs),
                        'timestamp': asyncio.get_event_loop().time()
                    }
                return st.session_state[cache_key]['result']
            return wrapper
        return decorator
