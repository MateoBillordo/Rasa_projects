from multiprocessing.dummy import Manager
from typing import List,Dict,Text, Optional, Any, Union, Tuple
from rasa.core.policies.policy import Policy
from rasa.shared.nlu.interpreter import NaturalLanguageInterpreter
from rasa.shared.core.trackers import DialogueStateTracker
from rasa.shared.core.generator import TrackerWithCachedStates
from rasa.core.constants import DEFAULT_POLICY_PRIORITY
from rasa.shared.core.constants import ACTION_LISTEN_NAME
from rasa.shared.core.domain import Domain
from rasa.core.featurizers.tracker_featurizers import TrackerFeaturizer
from rasa.shared.nlu.interpreter import NaturalLanguageInterpreter
from rasa.core.policies.policy import Policy, PolicyPrediction
from rasa.core.policies.policy import confidence_scores_for
from rasa.shared.nlu.constants import INTENT_NAME_KEY
from rasa.shared.core.trackers import DialogueStateTracker
from rasa.shared.core.generator import TrackerWithCachedStates
from rasa.shared.utils.io import is_logging_disabled
from rasa.core.constants import (
    DEFAULT_CORE_FALLBACK_THRESHOLD,
    RULE_POLICY_PRIORITY,
    POLICY_PRIORITY,
    POLICY_MAX_HISTORY,
)
from rasa.engine.storage.resource import Resource
from rasa.engine.recipes.default_recipe import DefaultV1Recipe
from rasa.engine.storage.storage import ModelStorage
from rasa.engine.graph import ExecutionContext

# from classes import Manager

# temporary constants to support back compatibility
MAX_HISTORY_NOT_SET = -1
OLD_DEFAULT_MAX_HISTORY = 5

@DefaultV1Recipe.register(
    DefaultV1Recipe.ComponentType.POLICY_WITHOUT_END_TO_END_SUPPORT, is_trainable=False
)
class ChatPolicy(Policy):
	def __init__(
			self,
        	config: Dict[Text, Any],
        	model_storage: ModelStorage,
        	resource: Resource,
        	execution_context: ExecutionContext,
        	featurizer: Optional[TrackerFeaturizer] = None,
        	lookup: Optional[Dict] = None,
		) -> None:

		config[POLICY_MAX_HISTORY] = None
		super().__init__(config, model_storage, resource, execution_context, featurizer)
		print ("ANTES:",self.priority)
		self.answered = False
		self.config["priority"] = 6
		print("DESPUES:",self.priority)
	def train(
			self,
			training_trackers: List[TrackerWithCachedStates],
			domain: Domain,
			**kwargs: Any,
	) -> Resource:
		"""Trains the policy on given training trackers.
        Args:
            training_trackers:
                the list of the :class:`rasa.core.trackers.DialogueStateTracker`
            domain: the :class:`rasa.shared.core.domain.Domain`
            interpreter: Interpreter which can be used by the polices for featurization.
        """
		pass

	def predict_action_probabilities(
			self,
			tracker: DialogueStateTracker,
			domain: Domain,
			rule_only_data: Optional[Dict[Text, Any]] = None,
			**kwargs: Any,
	) -> PolicyPrediction:
		print("")
		print("Especulando")
		result = self._default_predictions(domain)
		intent = str(tracker.latest_message.intent["name"])
		chat =  tracker.latest_message.metadata.get("message")["chat"]["type"]
		print(intent)
		print(chat)
		result = self._default_predictions(domain)
		if chat=="private":
			result = confidence_scores_for(str("no_contesta"), 0.0, domain)
		else:
			if not self.answered:
				if intent == "listos":
					result = confidence_scores_for(str("action_listos"), 1.0, domain)
				elif intent == "propuesta_fecha":
					result = confidence_scores_for(str("action_chequea_fecha"), 1.0, domain)
				elif intent == "confirmacion_reu":
					result = confidence_scores_for(str("action_confirmacion_reu"), 1.0, domain)
				else: 
					result = confidence_scores_for(str("no_contesta"), 1.0, domain)
				self.answered=True

			else:
				print("answered = FALSE")
				self.answered = False
				print("--------------------------")
			return self._prediction(result)

	def _metadata(self) -> Dict[Text, Any]:
		return {
			"priority": self.priority,
		}

	def get_default_config() -> Dict[Text, Any]:
		return {
			"priority": 7,
			"core_fallback_threshold": 0.3,
			"core_fallback_action_name": "action_default_fallback",
			"enable_fallback_prediction": False,
			"restrict_rules": True,
			"check_for_contradictions": False,
			"use_nlu_confidence_as_score": False,
		}

	@classmethod
	def _metadata_filename(cls) -> Text:
		return "test_policy.json"