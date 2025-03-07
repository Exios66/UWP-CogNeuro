# Computational Neuroscience Software

This directory contains resources for computational neuroscience software, including neural simulators, modeling frameworks, and tools for analyzing neuronal dynamics.

## Neural Simulation Environments

### Comparison of Neural Simulators

| Simulator | Level of Detail | Primary Use Cases | Language | Performance | Learning Curve | Notable Features |
|-----------|----------------|-------------------|----------|-------------|----------------|-----------------|
| NEURON | Detailed compartmental | Single neurons to small networks | C++/Python/HOC | High | Steep | Industry standard for detailed models, Blue Brain support |
| Brian2 | Flexible (point to detailed) | Teaching, rapid prototyping | Python | Moderate | Gentle | Equation-based syntax, ease of use |
| NEST | Point neuron | Large-scale networks | C++/Python | Very high | Moderate | Optimized for large networks, HPC support |
| ANNarchy | Rate to spiking | Neural networks, learning | Python/C++ | High | Moderate | GPU acceleration, plasticity rules |
| Genesis | Compartmental | Single neuron models | C/Script | Moderate | Steep | Long history, compartmental modeling |
| MOOSE | Multi-scale | Signaling pathways & electrophysiology | Python/C++ | Moderate | Moderate | Multi-scale modeling |
| PyNN | Abstracted | Multiple simulators interface | Python | Varies | Gentle | Simulator-agnostic interface |
| NetPyNE | Network-level | Complex networks with NEURON | Python | High | Moderate | High-level interface to NEURON |
| The Virtual Brain | Whole-brain | Large-scale brain dynamics | Python | Moderate | Moderate | Connectome-based modeling |

### Installation and Setup

#### NEURON

A widely used simulation environment for building and using computational models of neurons and networks.

```bash
# Ubuntu/Debian
sudo apt-get install neuron-simulator

# macOS (Homebrew)
brew install neuron

# pip installation (Python interface)
pip install neuron

# From source
git clone https://github.com/neuronsimulator/nrn.git
cd nrn
mkdir build
cd build
cmake .. -DCMAKE_INSTALL_PREFIX=~/neuron
make -j4
make install
```

#### Brian2

A free, open-source simulator for spiking neural networks written in Python.

```bash
# Basic installation
pip install brian2

# With additional features
pip install brian2 matplotlib jupyter
```

Example Brian2 code:

```python
from brian2 import *

# Define neurons
eqs = '''
dv/dt = (I-v)/tau : volt (unless refractory)
I : volt
tau : second
'''

G = NeuronGroup(2, eqs, threshold='v>0.8*I', reset='v=0*mV',
                refractory=5*ms, method='exact')
G.I = [1, 2] * mV
G.tau = [10, 100] * ms

# Define synapse
S = Synapses(G, G, 'w : volt', on_pre='v_post += w')
S.connect(i=0, j=1)
S.w = 0.5*mV

# Monitor
M = StateMonitor(G, 'v', record=True)

# Run simulation
run(100*ms)

# Plot results
plot(M.t/ms, M.v[0]/mV, label='Neuron 0')
plot(M.t/ms, M.v[1]/mV, label='Neuron 1')
xlabel('Time (ms)')
ylabel('v (mV)')
legend();
```

#### NEST

The Neural Simulation Tool for large-scale neural network models.

```bash
# Ubuntu/Debian
sudo apt-get install nest

# Using pip
pip install nest-simulator

# From source with custom options
git clone https://github.com/nest/nest-simulator.git
cd nest-simulator
mkdir build
cd build
cmake -DCMAKE_INSTALL_PREFIX:PATH=$HOME/nest ..
make
make install
```

## Single Neuron Modeling

### Compartmental Models

Compartmental models divide a neuron into connected sections to simulate spatial distribution of electrical signals.

#### Hodgkin-Huxley Model Implementation

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Hodgkin-Huxley parameters
C_m = 1.0  # membrane capacitance
g_Na = 120.0  # sodium conductance
g_K = 36.0  # potassium conductance
g_L = 0.3  # leak conductance
E_Na = 50.0  # sodium reversal potential
E_K = -77.0  # potassium reversal potential
E_L = -54.387  # leak reversal potential

# HH model equations
def HH_model(X, t, I_ext=10.0):
    V, m, h, n = X
    
    # Gating variable dynamics
    alpha_m = 0.1 * (V + 40.0) / (1.0 - np.exp(-(V + 40.0) / 10.0))
    beta_m = 4.0 * np.exp(-(V + 65.0) / 18.0)
    alpha_h = 0.07 * np.exp(-(V + 65.0) / 20.0)
    beta_h = 1.0 / (1.0 + np.exp(-(V + 35.0) / 10.0))
    alpha_n = 0.01 * (V + 55.0) / (1.0 - np.exp(-(V + 55.0) / 10.0))
    beta_n = 0.125 * np.exp(-(V + 65.0) / 80.0)
    
    # Currents
    I_Na = g_Na * m**3 * h * (V - E_Na)
    I_K = g_K * n**4 * (V - E_K)
    I_L = g_L * (V - E_L)
    
    # Differential equations
    dVdt = (I_ext - I_Na - I_K - I_L) / C_m
    dmdt = alpha_m * (1.0 - m) - beta_m * m
    dhdt = alpha_h * (1.0 - h) - beta_h * h
    dndt = alpha_n * (1.0 - n) - beta_n * n
    
    return [dVdt, dmdt, dhdt, dndt]

# Initial conditions
X0 = [-65.0, 0.05, 0.6, 0.32]  # V, m, h, n

# Time points
t = np.linspace(0, 50, 5000)

# Solve ODEs
X = odeint(HH_model, X0, t)
V = X[:, 0]

# Plot voltage trace
plt.figure(figsize=(10, 6))
plt.plot(t, V)
plt.xlabel('Time (ms)')
plt.ylabel('Membrane Potential (mV)')
plt.title('Hodgkin-Huxley Model: Action Potential')
plt.grid(True)
plt.show()
```

### Simpler Models

| Model | Complexity | Computational Cost | Biological Fidelity | Key Features |
|-------|------------|-------------------|---------------------|--------------|
| Hodgkin-Huxley | High | High | High | Accurate AP shape, channel dynamics |
| Morris-Lecar | Medium | Medium | Medium | Simpler than HH, still biophysical |
| FitzHugh-Nagumo | Low | Low | Low | Qualitative AP behavior, phase plane analysis |
| Izhikevich | Low | Very low | Medium | Diverse firing patterns, computationally efficient |
| Leaky Integrate-and-Fire | Very low | Very low | Very low | Most efficient, limited biological features |
| Adaptive Exponential IF | Low | Low | Medium | Good balance of efficiency and features |
| Generalized Integrate-and-Fire | Medium | Medium | Medium | Versatile, physiologically interpretable parameters |

#### Izhikevich Model Example

```python
import numpy as np
import matplotlib.pyplot as plt

# Simulation parameters
T = 1000  # ms
dt = 0.1  # ms
t = np.arange(0, T, dt)
n = len(t)

# Izhikevich model parameters for different neuron types
neuron_types = {
    'Regular Spiking': {'a': 0.02, 'b': 0.2, 'c': -65, 'd': 8},
    'Intrinsically Bursting': {'a': 0.02, 'b': 0.2, 'c': -55, 'd': 4},
    'Chattering': {'a': 0.02, 'b': 0.2, 'c': -50, 'd': 2},
    'Fast Spiking': {'a': 0.1, 'b': 0.2, 'c': -65, 'd': 2},
    'Low-Threshold Spiking': {'a': 0.02, 'b': 0.25, 'c': -65, 'd': 2},
}

# Create figure for plotting
plt.figure(figsize=(15, 10))

# Simulate each neuron type
for i, (name, params) in enumerate(neuron_types.items(), 1):
    # Initialize variables
    v = np.zeros(n)
    u = np.zeros(n)
    v[0] = -65  # Initial membrane potential
    u[0] = params['b'] * v[0]  # Initial recovery variable
    
    # Input current
    I = np.zeros(n)
    I[2000:] = 10  # Apply constant current after 200ms
    
    # Simulation loop
    for j in range(1, n):
        # Update membrane potential
        if v[j-1] >= 30:
            v[j] = params['c']
            u[j] = u[j-1] + params['d']
        else:
            dv = (0.04 * v[j-1]**2 + 5 * v[j-1] + 140 - u[j-1] + I[j-1]) * dt
            du = (params['a'] * (params['b'] * v[j-1] - u[j-1])) * dt
            v[j] = v[j-1] + dv
            u[j] = u[j-1] + du
    
    # Plot results
    plt.subplot(len(neuron_types), 1, i)
    plt.plot(t, v)
    plt.title(f"{name}: a={params['a']}, b={params['b']}, c={params['c']}, d={params['d']}")
    plt.ylabel('Membrane\nPotential (mV)')
    if i == len(neuron_types):
        plt.xlabel('Time (ms)')

plt.tight_layout()
plt.show()
```

## Network Modeling

### Network Types

| Network Type | Description | Applications | Tools |
|--------------|-------------|--------------|-------|
| Feed-forward | Information flows in one direction | Sensory processing, pattern recognition | Brian2, NEST, PyTorch |
| Recurrent | Information can flow in loops | Working memory, temporal processing | NEST, Brian2, Tensorflow |
| Small-world | High clustering, short path lengths | Cortical networks | NetworkX, NEST |
| Scale-free | Power-law degree distribution | Brain connectome modeling | NetworkX, The Virtual Brain |
| Reservoir | Large recurrent networks as dynamic reservoirs | Temporal processing, speech recognition | Reservoirpy, Brian2 |
| Oscillatory | Networks displaying rhythmic activity | Brain rhythms, synchronization | Brian2, NEST |

### Creating a Balanced Network in NEST

```python
import nest
import numpy as np
import matplotlib.pyplot as plt

# Reset NEST kernel
nest.ResetKernel()

# Set simulation parameters
dt = 0.1    # simulation step (ms)
simtime = 1000.0  # simulation time (ms)

# Network parameters
N_ex = 8000  # number of excitatory neurons
N_in = 2000  # number of inhibitory neurons
N_neurons = N_ex + N_in

# Connection parameters
J_ex = 0.1  # excitatory weight (mV)
J_in = -0.5  # inhibitory weight (mV)
p = 0.1  # connection probability

# Create neurons
neuron_params = {
    "V_m": -65.0,
    "E_L": -65.0,
    "C_m": 1.0,
    "tau_m": 20.0,
    "t_ref": 2.0,
    "V_th": -50.0,
    "V_reset": -65.0,
}

neurons = nest.Create("iaf_psc_alpha", N_neurons, params=neuron_params)
ex_neurons = neurons[:N_ex]
in_neurons = neurons[N_ex:]

# Create spike detectors
spike_detector = nest.Create("spike_recorder")
nest.Connect(neurons, spike_detector)

# Create Poisson input (external drive)
poisson_generator = nest.Create("poisson_generator", params={"rate": 20000.0})
nest.Connect(poisson_generator, neurons, syn_spec={"weight": 0.1})

# Create internal connections
conn_dict = {"rule": "fixed_probability", "p": p}

# Excitatory connections
nest.Connect(
    ex_neurons, neurons,
    conn_dict,
    syn_spec={"weight": J_ex}
)

# Inhibitory connections
nest.Connect(
    in_neurons, neurons,
    conn_dict,
    syn_spec={"weight": J_in}
)

# Simulate network
nest.Simulate(simtime)

# Extract and plot spike data
events = nest.GetStatus(spike_detector, "events")[0]
spikes = events["senders"]
times = events["times"]

plt.figure(figsize=(12, 6))
plt.plot(times, spikes, "k.", markersize=1)
plt.xlabel("Time (ms)")
plt.ylabel("Neuron ID")
plt.title("Balanced Network Activity")
plt.show()

# Calculate firing rates
n_bins = 100
rate_ex = np.histogram(
    times[spikes <= N_ex], bins=n_bins, range=(0, simtime)
)[0] / (simtime / n_bins) / N_ex * 1000
rate_in = np.histogram(
    times[spikes > N_ex], bins=n_bins, range=(0, simtime)
)[0] / (simtime / n_bins) / N_in * 1000

# Plot rates
plt.figure(figsize=(12, 6))
plt.plot(np.linspace(0, simtime, n_bins), rate_ex, label="Excitatory")
plt.plot(np.linspace(0, simtime, n_bins), rate_in, label="Inhibitory")
plt.xlabel("Time (ms)")
plt.ylabel("Rate (Hz)")
plt.legend()
plt.title("Population Rates")
plt.show()
```

## Plasticity Models

### Synaptic Plasticity Types

| Plasticity Type | Time Scale | Key Features | Models |
|-----------------|------------|--------------|--------|
| STDP | Short-term | Timing-dependent weight changes | Classic STDP, Triplet STDP |
| Homeostatic Plasticity | Long-term | Stabilizes network activity | Synaptic scaling, Intrinsic plasticity |
| Short-Term Plasticity | Milliseconds to seconds | Dynamic synaptic efficacy | Tsodyks-Markram model |
| Reward-Modulated STDP | Variable | Learning based on reward signals | R-STDP, Eligibility traces |
| Structural Plasticity | Long-term | Creation/elimination of synapses | Network rewiring models |
| STDP + Consolidation | Mixed | Combines fast changes with slow consolidation | Cascade models |

### STDP Implementation in Brian2

```python
from brian2 import *

# Neuron parameters
N_input = 100
N_output = 1
input_rate = 10*Hz
weight_max = 1

# Set up simulation
defaultclock.dt = 0.1*ms
runtime = 100*second

# Define neurons
eqs = '''
dv/dt = (I - v)/tau : 1
I : 1
tau : second
'''

# Input neurons (Poisson spiking)
input_neurons = PoissonGroup(N_input, rates=input_rate)

# Output neuron (LIF)
output_neuron = NeuronGroup(N_output, eqs, threshold='v>1', reset='v=0', 
                           method='exact', refractory=5*ms)
output_neuron.tau = 10*ms

# Create synapses with STDP
S = Synapses(input_neurons, output_neuron, 
             '''
             w : 1 (shared)
             dapre/dt = -apre/taupre : 1 (event-driven)
             dapost/dt = -apost/taupost : 1 (event-driven)
             ''',
             on_pre='''
             v_post += w
             apre += Apre
             w = clip(w + apost, 0, weight_max)
             ''',
             on_post='''
             apost += Apost
             w = clip(w + apre, 0, weight_max)
             ''')
S.connect()

# STDP parameters
S.w = 0.5
taupre = 20*ms
taupost = 20*ms
Apre = 0.01
Apost = -0.01

# Record spikes and weights
spike_mon = SpikeMonitor(output_neuron)
weight_mon = StateMonitor(S, 'w', record=np.arange(20))

# Run simulation
run(runtime)

# Plot results
plt.figure(figsize=(10, 8))

plt.subplot(211)
plt.plot(spike_mon.t/second, spike_mon.i, '.k')
plt.xlabel('Time (s)')
plt.ylabel('Neuron index')
plt.title('Output Spikes')

plt.subplot(212)
plt.plot(weight_mon.t/second, weight_mon.w.T)
plt.xlabel('Time (s)')
plt.ylabel('Weight')
plt.title('Synaptic Weights (20 synapses shown)')

plt.tight_layout()
plt.show()
```

## Neural Mass Models

Neural mass models simulate the average activity of neuronal populations rather than individual neurons.

### Model Types

| Model | Description | Applications | Key Features |
|-------|-------------|--------------|-------------|
| Wilson-Cowan | Classic firing rate model | Basic oscillations, stability | Two coupled populations (E-I) |
| Jansen-Rit | Cortical column model | EEG generation, alpha rhythms | Three populations, realistic PSPs |
| Wong-Wang | Decision-making model | Working memory, decisions | Reduced from spiking model |
| Neural Field | Spatially continuous | Wave propagation, patterns | PDE-based, spatial patterns |
| Kuramoto | Phase oscillator model | Synchronization | Simple yet powerful |
| The Virtual Brain | Multi-scale brain model | Whole-brain dynamics | Based on connectome |

### Example: Wilson-Cowan Model

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import odeint

# Wilson-Cowan model parameters
tau_e = 10.0  # ms, time constant for excitatory population
tau_i = 20.0  # ms, time constant for inhibitory population
c_ee = 16.0   # excitatory to excitatory coupling 
c_ei = 12.0   # inhibitory to excitatory coupling
c_ie = 15.0   # excitatory to inhibitory coupling
c_ii = 3.0    # inhibitory to inhibitory coupling
P_e = 1.0     # external input to excitatory population
P_i = 0.0     # external input to inhibitory population
r_e_max = 1.0  # maximum firing rate of excitatory population
r_i_max = 1.0  # maximum firing rate of inhibitory population

# Sigmoid function
def sigmoid(x, theta, beta):
    return 1.0 / (1.0 + np.exp(-beta * (x - theta)))

# Wilson-Cowan equations
def wilson_cowan(state, t, P_e, P_i):
    r_e, r_i = state
    
    # Input to each population
    input_e = c_ee * r_e - c_ei * r_i + P_e
    input_i = c_ie * r_e - c_ii * r_i + P_i
    
    # Activation functions
    F_e = sigmoid(input_e, 4.0, 1.0)
    F_i = sigmoid(input_i, 3.7, 1.0)
    
    # Differential equations
    dr_e_dt = (-r_e + (r_e_max - r_e) * F_e) / tau_e
    dr_i_dt = (-r_i + (r_i_max - r_i) * F_i) / tau_i
    
    return [dr_e_dt, dr_i_dt]

# Parameter space exploration
P_e_values = np.linspace(0, 5, 20)
P_i_values = np.linspace(0, 5, 20)
r_e_final = np.zeros((len(P_e_values), len(P_i_values)))
r_i_final = np.zeros((len(P_e_values), len(P_i_values)))

# Time points for integration
t = np.linspace(0, 300, 3000)  # 300 ms, 0.1 ms resolution

# Initial conditions (low activity)
state0 = [0.1, 0.1]  # [r_e, r_i]

# Explore parameter space
for i, P_e in enumerate(P_e_values):
    for j, P_i in enumerate(P_i_values):
        # Solve ODEs
        state = odeint(wilson_cowan, state0, t, args=(P_e, P_i))
        
        # Store final state
        r_e_final[i, j] = state[-1, 0]
        r_i_final[i, j] = state[-1, 1]

# Plot phase space
plt.figure(figsize=(12, 5))

plt.subplot(121)
plt.imshow(r_e_final, origin='lower', extent=[P_i_values[0], P_i_values[-1], 
                                             P_e_values[0], P_e_values[-1]],
           aspect='auto', cmap='viridis')
plt.colorbar(label='Excitatory Rate')
plt.xlabel('P_i')
plt.ylabel('P_e')
plt.title('Excitatory Activity')

plt.subplot(122)
plt.imshow(r_i_final, origin='lower', extent=[P_i_values[0], P_i_values[-1], 
                                             P_e_values[0], P_e_values[-1]],
           aspect='auto', cmap='viridis')
plt.colorbar(label='Inhibitory Rate')
plt.xlabel('P_i')
plt.ylabel('P_e')
plt.title('Inhibitory Activity')

plt.tight_layout()
plt.show()

# Time series for a specific parameter set
P_e_specific = 2.5
P_i_specific = 0.0
state = odeint(wilson_cowan, state0, t, args=(P_e_specific, P_i_specific))
r_e = state[:, 0]
r_i = state[:, 1]

plt.figure(figsize=(10, 4))
plt.plot(t, r_e, label='Excitatory')
plt.plot(t, r_i, label='Inhibitory')
plt.xlabel('Time (ms)')
plt.ylabel('Firing Rate')
plt.title(f'Wilson-Cowan Dynamics (P_e={P_e_specific}, P_i={P_i_specific})')
plt.legend()
plt.grid(True)
plt.show()
```

## Resources and Learning Materials

### Textbooks and References

- "Theoretical Neuroscience" by Peter Dayan and L.F. Abbott
- "Dynamical Systems in Neuroscience" by Eugene M. Izhikevich
- "Principles of Computational Modelling in Neuroscience" by David Sterratt et al.
- "Neuronal Dynamics" by Wulfram Gerstner et al. (with [online course](https://neuronaldynamics.epfl.ch/))
- "From Computer to Brain" by William W. Lytton

### Online Courses

- [Computational Neuroscience](https://www.coursera.org/learn/computational-neuroscience) on Coursera
- [Brain Inspired Cognitive Architectures](https://www.edx.org/course/brain-inspired-cognitive-architectures) on edX
- [Neuromatch Academy](https://compneuro.neuromatch.io/) - Computational Neuroscience summer school
- [Neuronal Dynamics](https://neuronaldynamics.epfl.ch/) by EPFL

### Journals and Conferences

- Journal of Computational Neuroscience
- Neural Computation
  - PLOS Computational Biology
- Frontiers in Computational Neuroscience
- Computational Brain & Behavior
- Computational Neuroscience Meeting (CNS)
- Neural Information Processing Systems (NeurIPS)

### Software Tutorials and Documentation

- [Brian2 Documentation](https://brian2.readthedocs.io/)
- [NEURON Tutorials](https://neuron.yale.edu/neuron/docs/tutorials)
- [NEST Simulator Documentation](https://nest-simulator.readthedocs.io/)
- [The Virtual Brain Documentation](https://docs.thevirtualbrain.org/)
- [NetPyNE Tutorials](http://netpyne.org/tutorials.html)

## Future Directions

### Bridging Scales

Recent developments are focused on multi-scale modeling, connecting:

- Molecular dynamics
- Cellular biophysics
- Network dynamics
- Cognitive function

### Integration with Machine Learning

- Using ML to fit complex models to data
- Implementing biologically plausible learning rules
- Neural architectures inspired by brain organization

### Reproducible Modeling

- Model sharing platforms (ModelDB, Open Source Brain)
- Standardized descriptions (NeuroML, SONATA)
- Containerization for reproducible environments
