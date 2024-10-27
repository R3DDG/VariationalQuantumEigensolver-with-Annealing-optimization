use rand::Rng;
use std::fs::File;
use std::io::prelude::*;
use std::collections::HashMap;

struct Qbit {
  amplitude: f64,
  position: i32,
  coin_state: bool,
}

fn main() {
  quantum_walks();
}


fn quantum_walks() {
  let mut file = File::create("quantum-walks2.txt").unwrap();
  let mut states: HashMap<String, Qbit> = HashMap::new();
  let borders = (-15, 15);
  let mut rng = rand::thread_rng();

  let mut entropy: f64 = 0.0;

  states.insert(get_qbit_key(0, false), Qbit {
    amplitude: 1.0,
    position: 0,
    coin_state: false,
  });
  for n in (10..=100).step_by(10) {
    for _ in 1..=n {
      let mut temp_states: HashMap<String, Qbit> = HashMap::new();

      let mut insert_qbit_to_hash_map = |key: String, qbit: Qbit| {
        match temp_states.get(&key) {
          None => {
            temp_states.insert(key, qbit);
          }
          Some(currentQbit) => {
            let amplitude: f64 = currentQbit.amplitude + qbit.amplitude;
            // если  по итогу получили ноль, чтобы в следующих итерациях не пробегать по этому кубиту.И чтобы там не валялось значение с нулевой ампоитудой, то мы его удаляем
            if amplitude == 0.0 {
              temp_states.remove(&*key);
            } else {
              temp_states.insert(key, Qbit {
                amplitude: currentQbit.amplitude + qbit.amplitude,
                coin_state: qbit.coin_state,
                position: qbit.position,
              });
            }
          }
        }
      };
      let p = rng.gen::<f32>();

      for state in states.values() {

        let qbits: (Qbit, Qbit);

        if p > 0.9 {
          qbits = unit_transformation(state, p as f64);
        } else {
          qbits = hadamar(state);
        }

        let shiftedFirstQbit = coin_transformation(qbits.0, borders);
        let shiftedSecondQbit = coin_transformation(qbits.1, borders);

        let first_qbit_key = get_qbit_key(shiftedFirstQbit.position, shiftedFirstQbit.coin_state);
        let second_qbit_key = get_qbit_key(shiftedSecondQbit.position, shiftedSecondQbit.coin_state);

        insert_qbit_to_hash_map(first_qbit_key, shiftedFirstQbit);
        insert_qbit_to_hash_map(second_qbit_key, shiftedSecondQbit);
      }

      states = temp_states;
    }


    for state in states.values() {
      let probability = f64::powf(state.amplitude, 2.0);

      if probability != 0.0 {
        entropy -= probability * probability.ln();
      }
    }
    writeln!(&mut file, "n: {} s: {}", n, entropy);

    entropy = 0.0;
  }
}

fn get_qbit_key(position: i32, coin_state: bool) -> String {
  coin_state.to_string() + ";" + &*position.to_string()
}

fn hadamar(initial_qbit: &Qbit) -> (Qbit, Qbit) {
  return if initial_qbit.coin_state == false {
    (
      Qbit {
        amplitude: initial_qbit.amplitude * (1.0 / 2_f64.sqrt()),
        position: initial_qbit.position,
        coin_state: false,
      },
      Qbit {
        amplitude: initial_qbit.amplitude * (1.0 / 2_f64.sqrt()),
        position: initial_qbit.position,
        coin_state: true,
      })
  } else {
    (
      Qbit {
        amplitude: initial_qbit.amplitude * (1.0 / 2_f64.sqrt()),
        position: initial_qbit.position,
        coin_state: false,
      },
      Qbit {
        amplitude: initial_qbit.amplitude * (1.0 / 2_f64.sqrt()) * -1.0,
        position: initial_qbit.position,
        coin_state: true,
      })
  };
}

fn unit_transformation(initial_qbit: &Qbit, p: f64) -> (Qbit, Qbit) {
  return if initial_qbit.coin_state == false {
    (
      Qbit {
        amplitude: initial_qbit.amplitude * p.sqrt(),
        position: initial_qbit.position,
        coin_state: false,
      },
      Qbit {
        amplitude: initial_qbit.amplitude * (-1.0 *(1.0 - p).sqrt()),
        position: initial_qbit.position,
        coin_state: true,
      })
  } else {
    (
      Qbit {
        amplitude: initial_qbit.amplitude * (1.0 *(1.0 - p).sqrt()),
        position: initial_qbit.position,
        coin_state: false,
      },
      Qbit {
        amplitude: initial_qbit.amplitude * p.sqrt(),
        position: initial_qbit.position,
        coin_state: true,
      })
  };
}

fn coin_transformation(initial_qbit: Qbit, borders: (i32, i32)) -> Qbit {
  return if initial_qbit.coin_state {
    if initial_qbit.position == borders.1 { // проверка на то, что мы коснулись правой границы, тогда двигаем частицу влево
      Qbit {
        amplitude: initial_qbit.amplitude,
        coin_state: initial_qbit.coin_state,
        position: initial_qbit.position - 1,
      }
    } else {
      Qbit {
        amplitude: initial_qbit.amplitude,
        coin_state: initial_qbit.coin_state,
        position: initial_qbit.position + 1,
      }
    }
  } else {
    if initial_qbit.position == borders.0 {  // проверка на то, что мы коснулись левой границы, тогда двигаем частицу вправо
      Qbit {
        amplitude: initial_qbit.amplitude,
        coin_state: initial_qbit.coin_state,
        position: initial_qbit.position + 1,
      }
    } else {
      Qbit {
        amplitude: initial_qbit.amplitude,
        coin_state: initial_qbit.coin_state,
        position: initial_qbit.position - 1,
      }
    }
  };
}

fn coin_transformation_old(initial_qbit: Qbit, borders: (i32, i32)) -> Qbit {
  return if initial_qbit.coin_state {
      Qbit {
        amplitude: initial_qbit.amplitude,
        coin_state: initial_qbit.coin_state,
        position: initial_qbit.position + 1,
      }
  } else {
      Qbit {
        amplitude: initial_qbit.amplitude,
        coin_state: initial_qbit.coin_state,
        position: initial_qbit.position - 1,
      }
  };
}

fn simple_walks() {
  let A: i32 = -20;
  let B: i32 = 20;
  let N = 100;
  let mut file = File::create("simple_walks.txt").unwrap();

  let mut map: HashMap<i32, f64> = HashMap::new();
  let mut rng = rand::thread_rng();

  for n in (10..11) {
    let mut p = 0.1;
    let mut x = 0;
    let mut S = 0.0;
    while p <= 0.9 {
      for i in 0..N { // move point
        for k in 0..=n {
          let r = rng.gen::<f32>();
          if p < r {
            if x == B { x = x; } else { x += 1; }
          } else {
            if x == A { x = x; } else { x -= 1; }
          }
        }
        let count = map.entry(x).or_insert(0.0);
        *count += 1.0;
        x = 0;
      }
      for i in A..=B {
        if map.contains_key(&i) {
          let mut sumValue = map.get(&i).unwrap() / N as f64;
          S -= sumValue * (sumValue.ln() / 2_f64.log2())
        }
      }
      writeln!(&mut file, "Вероятность {} Энтропия {}", p, S);
      writeln!(&mut file, "{:?}", map);
      map.clear();
      p += 0.1;
      S = 0.0;
    }
  }
  println!("{:?}", map);
}