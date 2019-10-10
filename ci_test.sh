#!/bin/bash

# Prep the results.markdown file
echo "Results for "$JOB_NAME > results.markdown
echo "" >> results.markdown
echo 'Module | Instance | Kubernetes' >> results.markdown
echo '-----|-------|------' >> results.markdown

# Clone and prep Stockpile
git clone https://github.com/cloud-bulldozer/stockpile.git

cp stockpile/ci/all.yml stockpile/group_vars/all.yml

sed -i 's/\/tmp\/stockpile.json/\/tmp\/stockpile_scribe.json/' stockpile/group_vars/all.yml
sed -i 's/\/tmp\/container/\/tmp\/scribe_container/' stockpile/group_vars/all.yml

cd stockpile

echo "Running Stockpile"
ansible-playbook -i ci/hosts stockpile.yml -e kube_config=/root/.kube/config

cd ..

module_list=`ls transcribe/scribe_modules/*.py | grep -v __ | grep -v base_scribe_module | sed 's/.py//' | awk -F "/" '{print $3}'`

echo "Scribe module list: "$module_list

# Create python3 virt env for the test
python3 -m venv ci_test

source ci_test/bin/activate

# Install scribe into the venv
pip3 install -e .

rc=0

# Test against the local (instance) data
python3 -m scribe -t stockpile -ip /tmp/stockpile_scribe.json > scribe_out
scribe_rc=$?

if [[ $scribe_rc -eq 1 ]]
then
  echo "Scribe failed to run checking instance output. Exiting"
  exit 1
fi

# Test against against the backpack created data
for cont_file in `ls /tmp/scribe_container/backpack*`
do
  echo $cont_file
  python3 -m scribe -t stockpile -ip $cont_file > scribe_cont_out
  scribe_cont_rc=$?

  if [[ $scribe_cont_rc -eq 1 ]]
  then
    echo "Scribe failed to run checking container output. Exiting"
    exit 1
  fi
done


echo "Full scribe instance output:"
cat scribe_out
echo ""
echo ""
echo ""
echo "Full scribe container output:"
cat scribe_cont_out
echo ""
echo ""
echo "Scribe Module Results:"

for module in $module_list
do
  grep $module" is not part" scribe_out
  my_inst_rc=$?
  grep $module" is not part" scribe_cont_out
  my_cont_rc=$?

  if [ $my_inst_rc -eq 1 ]
  then
    echo -n $module": Passed Instance"
    echo -n $module"|Pass" >> results.markdown
  else
    echo -n $module": Failed Instance"
    echo -n $module"|Fail" >> results.markdown
    rc=1
  fi
  if [ $my_cont_rc -eq 1 ]
  then
    echo " | Passed Kubernetes"
    echo "|Pass" >> results.markdown
  else
    echo " |  Failed Kubernetes"
    echo "|Fail" >> results.markdown
    rc=1
  fi
done

deactivate

rm -rf stockpile ci_test /tmp/scribe_container

exit $rc
