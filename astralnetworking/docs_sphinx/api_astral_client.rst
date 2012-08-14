Astral client classes
...........................

.. module:: astral.client
    
.. module:: astral.client.gameclient

.. autoclass:: GameClient()
    :members:
    
    .. automethod:: __init__()
    
    >>> from astral.client.gameclient import GameClient
    >>> client = GameClient()
    >>> print client.running
    True
    
.. module:: astral.client.local