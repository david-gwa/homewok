## phyiscal vs virtual 

算法验证的四个维度： 运行通过， 运行正确， 算法性能， 算法可扩展性
算法测试的四个阶段： unit test, functional test, subsystem test, system integration test 
测试对应四类场景：       \    ,     \          ,  benchmark test scenario ,  miles/scenario coverage 

#### physical/virtual world 

case1) from physical world to physical sensor

联合真值系统，将physical sensor当做 device under test(DUT), 用以测试DUT传感器的性能指标、性能边界、传感器遮挡、失效后对fusion的影响。

case2) from virtual world to physical sensor 

 暗箱测试，投屏可以是 虚拟渲染或真实数据注入

#### physical/virtual sensor 

case3) from virtual world to virtual sensor 

依赖：建立传感器模型(virtual sensor model): 理想传感器、满足统计特征的传感器、物理级传感器模型

理想传感器模型、及满足统计特征的传感器较容易建立。当前传感器测试小组具有满足统计特征的传感器参数。

有了传感器模型，可建立闭环。用以验证下游fusion模块能否正确工作。

理想情况下，fusion模块对 virtual sensor perception 还是 physical sensor perception 应该不敏感。相反， virtual sensor (model) perception 更容易获取，方便验证fusion模块。

对于sensor验证的场景，可以依据sensor测试组的定义做。


#### physical/virtual perception data to fusion 

用以验证fusion模块运行准确率，及性能边界、失效处理等

case 4) from virtual sensor perception data to fusion 

virtual world里面，可以很容易建立“真值传感器"，再与fusion output 对比，验证fusion准备率。但这又要求对physical world 的建模和渲染逼真。


case 5) from physical sensor perception data to fusion 

当前该方法用于fusion回放验证，但当前physical 数据量较小。
physical数据采集，同时会包含真值数据。fusion 输出与真值对象对比，即可验证fusion模块准确率。

physical perception data的另一个价值是发掘edge case，用以完善scenario lib。

对于大批量回传链路建立后，edge case physical sensor data 回收可以形成闭环。此时，基于完全physical perception data 的开环logsim 对于 fusion 迭代的效益将非常明显。

注明：edge case 是那些non-normal perception/fusion case。但是怎么发掘non-normal perception case ? 对于fusion好坏的评价，只有fusion output 与 真值比较可知。大批量回传链路，缺乏真值标签。可以以比较稳定的me传感器当真值参照，对fusion output效验。

或者，在大批量回传链路闭环开始回传数据前，必须实现可靠性非常高的"类真值"传感器。用me或ibeo inext作为"类真值“传感器的坏处是，me或inext的稳定性、精度上限，就是融合算法的上限。


fusion 测试验证总结： fusion 验证需要真值，不论是物理采集真值，还是virtual GT sensor生成真值。1) 物理采集真值，只适用于R&D阶段，小规模数据，对大批量数据回传建立后，缺乏使用方法。2) 使用virtual GT sensor, 较容易拿到sim world 里面的标注真值，但要求对物理环境的建模逼真，否则真值”不真“。

还有一个观点， fusion模块性能是确定性的。使用真值系统，在研发阶段，做到fusion算法运行可靠及鲁棒，量产后不再需要对fusion做验证。而对于量产后的fusion edge case，需要 case by case 论证。

同样，所有传感器遮挡、失效等情况导致的fusion算法问题，应该在研发阶段解决。对于量产后发现的sensor 造成的fusion edge case 需要case by case 论证。


#### planning 

对决策好坏的评价是非常主观的，相比融合对比真值，具有客观性。

理想情况下，planning模块，对fusion output是来自真实世界，还是virtual 环境应该不敏感。对planning模块评价，理应要求前端fusion模块已稳定，不应该把fusion的问题，延迟到planning环节。

##### planning 评价定量

	planning评价有很大主观性。 一方面，如何将主观性评价尽可能量化， 另一方面，基于rss可以给出planning评价的边界。

case 6) from sim fusion output to planning 

	对于验证planning，非常有效。 SiL不论基于PreScan，还是LGSVL，对planning验证都是非常高效的。
	当前，planning算法开发过程，采用PreScan搭建的场景验证，对于验证planning算法可以正确工作的简单参数化场景，具有较好的测试能力。
	
	对于复杂动态场景，及真实人-车交互场景，及其他覆盖性、corner case验证，依赖大规模仿真。
	
	virtual world(digital twins of physical world)里面，如果agents具有符合真实世界驾驶员习惯的驾驶行为，可以较好的验证planning的性能。当然，这就要求micro traffic flow, agents driving behavior 必须能从真实场景中学习到(imitation learning)，参数化的planning验证场景，只具有basic 验证能力。
	
	前述，融合性能评价具有客观性，而planning评价主观性非常多，具有很大开放性，也是planning需要大规模测试的原因之一。
	闭环sim训练场，迭代的planning算法，首先需要在闭环-sim训练场通过，才能下发实车。当然sim训练场，可以直接基于physical fusion output建立，而不是virtual world fusion output.
	

case 7) from physical fusion output to planning 

	前述，当前planning还没有形成实车数据采集-replay-logsim的数据闭环。主要原因，planning开发还处于functional test阶段。 但是，大批量数据闭环是必然。
	
	大批量数据，对planing算法迭代及验证的意义：
	
	1) 更丰富的planning 场景库, 通过大批量数据，可以detect more edge cases, 要求数据平台具有场景提取、泛化能力。
	2) 训练agent/ego driving behavior 更符合实际人类驾驶员的驾驶决策习惯
			

#### control 测试验证

 control 与物理车辆响应息息相关。比较显著的问题，如，响应延迟、响应精度不够等。

 理想情况下，planning对下游control不敏感。不论是实车、还是仿真环境中的动力学模型，planning输出到control 响应，与planning自身是独立的。 

case 8) from planning to virtual vehicle(vehicle dynamic) 
	
	要求高精度的vehicle dyanmics模型，否则virtual vehicle响应与实车响应会有不同，影响sim的可靠性。
	
case 9) from planning to physical vehicle 

	ViL


