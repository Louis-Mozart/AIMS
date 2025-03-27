function [testclass, t, wHidden, wOutput] = ...
  mlp_template(traindata, trainclass, testdata, maxEpochs)
% Template for implementing a shallow multilayer perceptron network

N = size(traindata, 2);
d = size(traindata, 1);
classes = max(trainclass);

if ~exist('maxEpochs', 'var')
  maxEpochs = 100000;
end

% Initialisation
hidden = 16; % number of hidden layer neurons
J = zeros(1,maxEpochs); % loss function value vector initialisation
rho = 10^-4; % learning rate

trainOutput = zeros(classes, N);
for i = 1:N
  trainOutput(trainclass(i), i) = 1;
end

extendedInput = [traindata; ones(1, N)];
wHidden = (rand(d+1, hidden)-0.5) / 10;
wOutput = (rand(hidden+1, classes)-0.5) / 10;

x = extendedInput;

fh1 = figure;
t = 0;
while 1 % iterative training "forever"
  t = t+1;
  
  % Feed-forward operation
  vHidden = wHidden'*x; % hidden layer net activation
  yHidden = activate(vHidden); % hidden layer activation function

  yHidden = [yHidden;ones(1,N)]; % hidden layer extended output

  vOutput = wOutput'*yHidden; % output layer net activation
  yOutput = vOutput; % output layer output without activation f
    
  J(t) = 1/2*sum((trainOutput-yOutput).^2,'all'); % loss function evaluation

  if (mod(t, 1000) == 0) % Plot training error, but not for every epoch
    semilogy(1:t, J(1:t));
    title(sprintf('Training (epoch %d)', t));
    ylabel('Training error');
    drawnow;
  end
  
  if J(t) < eps % the learning is good enough
    break;
  end
  
  if t == maxEpochs % too many epochs would be done
    break;
  end
  
  if t > 1 % this is not the first epoch
    if norm(J(t)-J(t-1)) < eps % the improvement is small enough
      break;
    end
  end
  
  % Update the sensitivities and the weights
  deltaOutput = (yOutput - trainOutput);
  deltawOutput = -rho*yHidden*deltaOutput';
  
  deltaHidden = (wOutput(1:end-1,:)*deltaOutput) .* (1-yHidden(1:end-1,:).^2);
  deltawHidden = -rho * x * deltaHidden';
  
  wOutput = wOutput + deltawOutput;
  wHidden = wHidden + deltawHidden;
end

% Testing with the test data
N = size(testdata, 2);
extendedInput = [testdata; ones(1, N)];
x = extendedInput;

vHidden = wHidden'*x; % hidden layer net activation
yHidden = activate(vHidden); % hidden layer activation function

yHidden = [yHidden;ones(1,N)]; % hidden layer extended output

vOutput = wOutput'*yHidden; % output layer net activation
yOutput = vOutput; % output layer output without activation f

[tmp, testclass] = max(yOutput, [], 1);

function y = activate(x)
  y =tanh(x);
end
end
